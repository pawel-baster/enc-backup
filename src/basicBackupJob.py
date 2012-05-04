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

class BasicBackupJob(object):
    
    def __init__( self, logger, nameManager, backupProvider, synchronizer, updateEvery, dataFolder ):
        self.logger = logger
        self.nameManager = nameManager
        self.backupProvider = backupProvider
        self.synchronizer = synchronizer
        
        self.timestamp = int(time.time())
        self.updateEvery = updateEvery
                
        self.archivedFilesSize = 0;
        self.archivedFilesCount = 0
        self.restoredSettingsFileName = 'settings.dat.tmp'
        self.dataFolder = dataFolder
        self.lockFileName = os.path.join(dataFolder, datetime.datetime.today().strftime('%Y%m%d.lock'))        
    
    def backupModifiedFiles(self, root, excludePatterns, settings) :
        #lock          
        for filename in os.listdir(root):
            path = os.path.join(root, filename)
            if not self.isExcluded(path, excludePatterns):
                if os.path.isdir(path):
                    try:
                        if not os.path.islink(path):
                            self.backupModifiedFiles(path, excludePatterns, settings)
                        else:
                            self.logger.log('skipping symbolic link ' + path)
                    except IOError:
                        self.logger.log('could not enter directory: ' + path)
                elif os.path.isfile(path):
                    try:
                        size = os.path.getsize(path)
                        if settings['lastSearch'] <= os.path.getmtime(path) and size > 0:
                            dstName = self.nameManager.encodeName(path, settings)
                            self.backupProvider.backup(path, dstName)
                            self.archivedFilesSize += size
                            self.archivedFilesCount += 1
                    except IOError:
                        self.logger.log('could not encrypt: ' + path)
                else:
                    raise Exception('skipping strange file: {0}'.format(path))
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
        for filename in glob.glob(self.dataFolder + os.path.sep + '*.lock') :
            os.remove( filename )  
    
    def runBackup(self, inputFolder, excludePatterns, settingsFile) :
        if not self._isLocked():
            settings = self.loadSettings(settingsFile)
            if settings['lastSearch'] + self.updateEvery > self.timestamp:
                self.logger.log('backup not necessary at this moment')
            else: 
                if os.access(inputFolder, os.R_OK):
                    self.logger.log('last successful backup at {0}'.format(datetime.datetime.fromtimestamp(settings['lastSearch']).strftime('%Y-%m-%d %H:%M:%S')))
                    self.backupModifiedFiles(inputFolder, excludePatterns, settings)
                    settings['lastSearch'] = self.timestamp            
                    print 'archived files %d (%d B)' % (self.archivedFilesCount, self.archivedFilesSize)
                    print 'number of stored elements %d' % self.nameManager.getCount(settings)
                    self.cleanup(excludePatterns, settingsFile)
                    for key in settings['synchronized'].keys():
                        del settings['synchronized'][key]
                    self.saveSettings(settings, settingsFile)
                else:
                    print 'folder {0} does not exist or is inaccessible.'.format(inputFolder)
                
            self.synchronizer.synchronize(settings)
            self.saveSettings(settings, settingsFile)
            self._releaseLock()
        else:
            self.logger.log('Could not acquire lock')
    
    def runRestore(self, outputFolder) :
        tempSettingsFile = outputFolder + os.path.sep + self.restoredSettingsFileName
        self.backupProvider.restore('0', tempSettingsFile)
        settings = self.loadSettings(tempSettingsFile)
        os.remove(tempSettingsFile)
        errors = []
        for path in settings['mapping'] :
            try:
                self.logger.log('restoring ' + path)
                dst = outputFolder + path
                parent = os.path.dirname(dst)
                if not os.path.exists(parent):
                    os.makedirs(parent)
                self.backupProvider.restore(settings['mapping'][path]['filename'], dst)
            except IOError:
                msg = 'there was a problem with restoring {src} to {dst}: {exc}'.format(
                    src=settings['mapping'][path]['filename'],
                    dst=path,
                    exc=sys.exc_info()[1]
                )
                self.logger.log(msg)
                errors.append(msg)
        
        self.logger.log('Problems during restore:')
        for error in errors:
            self.logger.log(error)
                

    def listFiles(self, settingsFile):
        settings = self.loadSettings(settingsFile)
        for path in settings['mapping'] :
            print '%s -> %s' % (path, settings['mapping'][path]['filename'])
        print 'number of items: %d' % (len(settings['mapping'])) 

    def loadSettings(self, settingsFile) :
        if os.path.exists(settingsFile) :
            unpicklefile = open(settingsFile, 'r')
            settings = pickle.load(unpicklefile)
            unpicklefile.close()
        else :
            settings = {'lastId' : 1, 'mapping' : {}, 'lastSearch' : 0, 'synchronized' : {}} 
        return settings
    
    def saveSettings(self, settings, settingsFile) :
        if os.path.exists(settingsFile):
            shutil.copyfile(settingsFile, '{0}.old'.format(settingsFile))
        sfile = open(settingsFile, 'w')
        pickle.dump(settings, sfile)
        sfile.close()
        self.backupProvider.backup(settingsFile, '0') 

    def cleanup(self, excludePatterns, settingsFile, checkAll = False) :
        settings = self.loadSettings(settingsFile)
        for path, details in settings['mapping'].items() :
            if checkAll or details['nextCheck'] < self.timestamp:
                self.logger.log('checking ' + path)  
                if self.isExcluded(path, excludePatterns) or not os.path.exists(path):
                    #stats
                    try:
                        backupPath = os.path.join(self.backupProvider.getBackupFolder(), self.nameManager.encodeName(path, settings))
                        os.remove(backupPath)
                        del settings['mapping'][path]                    
                        self.logger.log('cleanup(): deleting a missing file entry:' + path + 'and corresponding file: ' + os.path.basename(backupPath))
                    except:
                        self.logger.log('problems while testing file ' + path)
                    
        self.saveSettings(settings, settingsFile)
             
        
        
