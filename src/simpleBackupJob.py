'''
Created on 2012-01-11

@author: pawel
'''

import os
import pickle
import time
import fnmatch

class SimpleBackupJob(object):
    
    def __init__( self, nameManager, backupProvider ):
        self.nameManager = nameManager
        self.backupProvider = backupProvider
        self.timestamp = int(time.time())
    
    def backupModifiedFiles(self, rootdir, excludePatterns, settings) :
        #lock          
        
        for root, subFolders, files in os.walk(rootdir):
            if not self.isExcluded(root, excludePatterns) :
                print 'looking for modified files in {0}'.format(root)
                for file in files:
                    # TODO if readable
                    path = os.path.join(root,file)
                    try:
                        if not self.isExcluded(path, excludePatterns): 
                            if settings['lastSearch'] < os.path.getmtime(path) :
                                #print 'backing up {file}'.format(file=path)
                                dstName = self.nameManager.translateName(path, settings)
                                self.backupProvider.backup(path, dstName)
                        else:
                            print 'ignoring file: {file}'.format(file=path)
                    except:
                        print 'could not access file: {file}'.format(file=path)
            else:
                print 'ignoring folder {folder}'.format(folder=root)
    
        settings['lastSearch'] = self.timestamp
        #print settings
        
    def isExcluded(self, path, excludePatterns):
        for pattern in excludePatterns:
            if fnmatch.fnmatch(path, pattern):
                return 1
        return 0
    
    def runBackup(self, inputFolder, excludePatterns, settingsFile) :
        settings = self.loadSettings(settingsFile)
        if settings['lastSearch'] + self.updateEvery > self.timestamp:
            print 'backup not necessary at this moment'
            return 
        
        if os.access(inputFolder, os.R_OK):
            self.backupModifiedFiles(inputFolder, excludePatterns, settings)
            self.saveSettings(settings, settingsFile)
            #TODO: check if files have not been removed & save (mind excluded)
        else:
            print 'folder {0} does not exist or is inaccessible.'.format(inputFolder)
    
    def runRestore(self, backupFolder, outputFolder) :
        # create temp file
        tempSettingsFile = '{0}{1}'.format(outputFolder, 'settings.dat.tmp')
        self.backupProvider.restore('{0}{1}'.format(backupFolder, '0'), tempSettingsFile)
        settings = self.loadSettings(tempSettingsFile)
        # TODO: remove tempSettingsFile
        #retrieve value in the same expression?
        for path in settings['mapping'] :
            print 'restoring {0}'.format(path)
            # TODO: mkdirs, check if readable
            self.backupProvider.restore('{0}{1}'.format(backupFolder, settings['mapping'][path]['filename']), '{0}{1}'.format(outputFolder, path))

    def loadSettings(self, settingsFile) :
        if os.path.exists(settingsFile) :
            unpicklefile = open(settingsFile, 'r')
            settings = pickle.load(unpicklefile)
            unpicklefile.close()
        else :
            settings = {'lastId' : 1, 'mapping' : {}, 'lastSearch' : 0} 
        return settings
    
    def saveSettings(self, settings, settingsFile) :
        file = open(settingsFile, 'w')
        pickle.dump(settings, file)
        file.close()
        self.backupProvider.backup(settingsFile, '0') 

        