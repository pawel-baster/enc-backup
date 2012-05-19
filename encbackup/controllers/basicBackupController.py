'''
Created on 2012-01-11

@author: pawel
'''

import os
import pickle
import time
import fnmatch
import datetime
import shutil
import glob
import sys

from controllerInterface import ControllerInterface

class BasicBackupController(ControllerInterface):
    
    def __init__( self, logger, nameManager, backupProvider, synchronizer, dataFolder):
        self.logger = logger
        self.nameManager = nameManager
        self.backupProvider = backupProvider
        self.synchronizer = synchronizer
        #self.self.dataFolder = dataFolder
        
        self.timestamp = int(time.time())
                
        self.archivedFilesSize = 0;
        self.archivedFilesCount = 0
        
        self.mappingFilePath = os.path.join(dataFolder, 'mapping.dat')
        self.statsFilePath = os.path.join(dataFolder, 'stats.dat')
        self.mappingBackupFileName = '0x0'
        self.statsBackupFileName = '0x1'
        self.lockFileName = os.path.join(dataFolder, datetime.datetime.today().strftime('%Y%m%d.lock'))
        self._errors = []

    def runBackup(self, inputFolders, outputFolder, excludePatterns, updateEvery) :
        if not self._isLocked():
            stats = self._loadSettingsFile(self.statsFilePath, {'lastSearch' : 0, 
                                                                'synchronized' : {},
                                                                'lastSynchronized' : {}})
            if stats['lastSearch'] + updateEvery > self.timestamp:
                self.logger.log('backup not necessary at this moment')
            else:
                mapping = self._loadSettingsFile(self.mappingFilePath, {'lastId' : 2, 'mapping' : {}})
                self.logger.log('last successful backup at {0}'.format(datetime.datetime.fromtimestamp(stats['lastSearch']).strftime('%Y-%m-%d %H:%M:%S')))
                for inputFolder in inputFolders:
                    if os.access(inputFolder, os.R_OK):
                        self._backupModifiedFiles(inputFolder, excludePatterns, stats, mapping)
                    else:
                        raise Exception('folder {0} does not exist or is inaccessible.'.format(inputFolder))
                
                stats['lastSearch'] = self.timestamp            
                print 'archived files %d (%d B)' % (self.archivedFilesCount, self.archivedFilesSize)
                print 'number of stored elements %d' % self.nameManager.getCount(mapping)
                self.cleanup(excludePatterns, mapping)
                for key in stats['synchronized'].keys():
                    del stats['synchronized'][key]
                    
                self._saveSettingsFile(self.mappingFilePath, self.mappingBackupFileName, mapping)
                
            self.synchronizer.synchronize(stats)
            self._saveSettingsFile(self.statsFilePath, self.statsBackupFileName, stats)            
                
            self._releaseLock()
        else:
            self.logger.log('Could not acquire lock')
            
        self._printErrors()
    
    def runRestore(self, backupFolder, outputFolder) :
        tempSettingsFile = self.mappingFilePath
        self.backupProvider.restore(self.mappingBackupFileName, tempSettingsFile)
        mapping = self._loadSettingsFile(tempSettingsFile, None)
        os.remove(tempSettingsFile)
        for path in mapping['mapping'] :
            try:
                self.logger.log('restoring ' + path)
                dst = outputFolder + path
                parent = os.path.dirname(dst)
                if not os.path.exists(parent):
                    os.makedirs(parent)
                self.backupProvider.restore(mapping['mapping'][path]['filename'], dst)
            except IOError:
                msg = 'there was a problem with restoring {src} to {dst}: {exc}'.format(
                    src=mapping['mapping'][path]['filename'],
                    dst=path,
                    exc=sys.exc_info()[1]
                )
                self.logger.log(msg)
                self._errors.append(msg)
        
        self._printErrors()
                
    def _printErrors(self):
        if len(self._errors) > 0:
            self.logger.log('Problems:')
            for error in self._errors:
                self.logger.log(error)


    def listFiles(self, settingsFile):
        settings = self.loadSettings(settingsFile)
        for path in settings['mapping'] :
            print '%s -> %s' % (path, settings['mapping'][path]['filename'])
        print 'number of items: %d' % (len(settings['mapping']))
    
    def _backupModifiedFiles(self, root, excludePatterns, stats, mapping) :
        #lock          
        for filename in os.listdir(root):
            path = os.path.join(root, filename)
            if not self.isExcluded(path, excludePatterns):
                if os.path.isdir(path):
                    try:
                        if not os.path.islink(path):
                            self._backupModifiedFiles(path, excludePatterns, stats, mapping)
                        else:
                            self.logger.log('skipping symbolic link ' + path)
                            self._errors.append('skipping symbolic link ' + path)
                    except IOError, e:
                        self.logger.log('could not enter directory: ' + path + ':')
                        self.logger.log('> %s' % e)
                        self._errors.append('could not enter directory: ' + path + ': %s' % e)
                elif os.path.isfile(path):
                    try:
                        size = os.path.getsize(path)
                        if stats['lastSearch'] <= os.path.getmtime(path) and size > 0:
                            dstName = self.nameManager.encodeName(path, mapping)
                            self.backupProvider.backup(path, dstName)
                            self.archivedFilesSize += size
                            self.archivedFilesCount += 1
                    except IOError, e:
                        self.logger.log('could not encrypt: ' + path)
                        self._errors.append('could not encrypt ' + path + ': %s' % e )
                else:
                    self.logger.log('skipping strange file: {0}'.format(path))
            else:
                self.logger.log('ignoring: ' + path)
        
    def isExcluded(self, path, excludePatterns):
        for pattern in excludePatterns:
            if fnmatch.fnmatch(path, pattern):
                return 1
        return 0
    
    def _isLocked(self):        
        if os.path.exists(self.lockFileName):
            return True
        else:
            # create empty file
            open(self.lockFileName, 'w').close()
            return False

    def _releaseLock(self):
        for filename in glob.glob(os.path.join(os.path.dirname(self.lockFileName), '*.lock')) :
            os.remove( filename )  
    
    def _unserialize(self, filePath):
        with open(filePath, 'r') as f:
            return pickle.load(f)
    
    def _loadSettingsFile(self, filepath, default) :
        if os.path.exists(filepath) :
            return self._unserialize(filepath)
        else :
            assert default, 'file {file} is missing, check if default is specified'.format(file=filepath)
            return default 
    
    def _saveSettingsFile(self, filepath, backupName, content) :
        if os.path.exists(filepath):
            shutil.copyfile(filepath, filepath + '.old')
        sfile = open(filepath, 'w')
        pickle.dump(content, sfile)
        sfile.close()
        self.backupProvider.backup(filepath, backupName) 

    def cleanup(self, excludePatterns, mapping, checkAll = False) :
        for path, details in mapping['mapping'].items() :
            if checkAll or details['nextCheck'] < self.timestamp:
                self.logger.log('checking ' + path)  
                if self.isExcluded(path, excludePatterns) or not os.path.exists(path):
                    #stats
                    try:
                        backupPath = os.path.join(self.backupProvider.getBackupFolder(), self.nameManager.encodeName(path, mapping))
                        os.remove(backupPath)
                        del mapping['mapping'][path]                    
                        self.logger.log('cleanup(): deleting a missing file entry:' + path + 'and corresponding file: ' + os.path.basename(backupPath))
                    except:
                        self.logger.log('problems while testing file ' + path)
                        self._errors.append('problems while testing file ' + path)
                    
        self._saveSettingsFile(self.mappingFilePath, self.mappingBackupFileName, mapping)
        
    def __del__(self):
        self._releaseLock()
    
        