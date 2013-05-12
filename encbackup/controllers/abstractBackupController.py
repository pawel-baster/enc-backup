'''
Created on Apr 9, 2013

@author: pb
'''

import abc
import datetime
import os

from helpers.logging import Logger
from controllerInterface import ControllerInterface

class Stats:
    def __init__(self):
        self.addedFilesSize = 0
        self.addedFilesCount = 0
        
        self.updatedFilesSize = 0
        self.updatedFilesCount = 0
        
        self.removedFilesSize = 0
        self.removedFilesCount = 0 

class AbstractBackupController(ControllerInterface):
    '''
    A backup controller that stores a tree of TreeNode objects 
    and compares it with the file system to prepare a list 
    of what has been added, removed or modified 
    '''
    __metaclass__ = abc.ABCMeta

    def __init__(self, lock, nameManager, backupProvider):
        self.lock = lock
        self.nameManager = nameManager
        self.backupProvider = backupProvider
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

    @abc.abstractmethod
    def loadState(self, inputFolder):
        raise Exception('not implemented')
    
    @abc.abstractmethod
    def saveState(self, inputFolder, state):
        raise Exception('not implemented')
    
    @abc.abstractmethod
    def isUpdatePending(self, state, updateEvery):
        raise Exception('not implemented')
    
    @abc.abstractmethod
    def backupFolder(self, inputFolder, outputFolder, excludePatterns, stats):
        raise Exception('not implemented')
    
    @abc.abstractmethod
    def printStats(self, stats):
        raise Exception('not implemented')

    def runBackup(self, inputFolders, outputFolder, excludePatterns, updateEvery) :
        if self.lock.acquireLock():
            Logger.log("Lock acquired")
            #try:
            state = self.loadState()
            if self.isUpdatePending(state, updateEvery):
                Logger.log("update pending")
                #Logger.log('last successful backup at {0}'.format(datetime.datetime.fromtimestamp(stats['lastSearch']).strftime('%Y-%m-%d %H:%M:%S')))
                stats = Stats()                    
                for inputFolder in inputFolders:                            
                    if os.access(inputFolder, os.R_OK):
                        self.backupFolder(state, inputFolders, outputFolder, excludePatterns, stats)
                    else:
                        raise Exception('folder {0} does not exist or is inaccessible.'.format(inputFolder))
            
                    self.printStats(stats)
                    self.saveState(state)
            else:
                Logger.log('backup not necessary at this moment')
                #Logger.log('next no sooner than {0}'.format(datetime.datetime.fromtimestamp(stats['lastSearch'] + updateEvery).strftime('%Y-%m-%d %H:%M:%S')))
        #except Exception, e:
            #    Logger.log("Error: %s" % e)
            #    raise e
            self.lock.releaseLock()
        else:
            Logger.log('Could not acquire lock')
   
    def runRestore(self, backupFoler, outputFolder) :
        raise Exception('not implemented')
        
    def listFiles(self, settingsFile):
        raise Exception('not implemented')