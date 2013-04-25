'''
Created on Apr 9, 2013

@author: pb
'''

import datetime
import os

from controllerInterface import ControllerInterface

class TreeStoreBackupController(ControllerInterface):
    '''
    A backup controller that stores a tree of TreeNode objects 
    and compares it with the file system to prepare a list 
    of what has been added, removed or modified 
    '''

    def __init__( self, logger, lock, nameManager, backupProvider, synchronizer, dataFolder):
          self.logger = logger
          self.lock = lock
#         self.nameManager = nameManager
#         self.backupProvider = backupProvider
#         self.synchronizer = synchronizer
#         
#         self.timestamp = int(time.time())
#                 
#         self.archivedFilesSize = 0;
#         self.archivedFilesCount = 0
#         
#         self.mappingFilePath = os.path.join(dataFolder, 'mapping.dat')
#         self.statsFilePath = os.path.join(dataFolder, 'stats.dat')
#         self.mappingBackupFileName = '0x0'
#         self.statsBackupFileName = '0x1'
#         self.lockFileName = os.path.join(dataFolder, datetime.datetime.today().strftime('%Y%m%d.lock'))
#         self._errors = []

    def loadState(self, inputFolder):
        raise Exception('not implemented')
    
    def saveState(self, inputFolder, state):
        raise Exception('not implemented')
    
    def isUpdatePending(self, state, updateEvery):
        raise Exception('not implemented')
    
    def backupFolder(self, inputFolder, outputFolder, excludePatterns, stats):
        raise Exception('not implemented')
    
    def printStats(self, stats):
        raise Exception('not implemented')

    def runBackup(self, inputFolders, outputFolder, excludePatterns, updateEvery) :
        if self.lock.acquireLock():
            try:
                state = self.loadState(outputFolder)
                if self.isUpdatePending(state, updateEvery):
                    #self.logger.log('last successful backup at {0}'.format(datetime.datetime.fromtimestamp(stats['lastSearch']).strftime('%Y-%m-%d %H:%M:%S')))
                    stats = Stats()                    
                    for inputFolder in inputFolders:                            
                        if os.access(inputFolder, os.R_OK):
                            self.backupFolder(state, inputFolder, outputFolder, excludePatterns, stats)
                        else:
                            raise Exception('folder {0} does not exist or is inaccessible.'.format(inputFolder))
                
                        self.printStats(stats)
                        self.saveState(state)
                else:
                    self.logger.log('backup not necessary at this moment')
                    #self.logger.log('next no sooner than {0}'.format(datetime.datetime.fromtimestamp(stats['lastSearch'] + updateEvery).strftime('%Y-%m-%d %H:%M:%S')))
            except:
                pass
            self.lock.releaseLock()
        else:
            self.logger.log('Could not acquire lock')
   
    def runRestore(self, backupFoler, outputFolder) :
        raise Exception('not implemented')
        
    def listFiles(self, settingsFile):
        raise Exception('not implemented')