'''
Created on Apr 9, 2013

@author: pb
'''

import fnmatch
import os

from controllerInterface import ControllerInterface
from encbackup.structures.tree import TreeNodeFile, TreeNodeDirectory

class TreeStoreBackupController(ControllerInterface):
    '''
    A backup controller that stores a tree of TreeNode objects 
    and compares it with the file system to prepare a list 
    of what has been added, removed or modified 
    '''

    def __init__( self, logger, nameManager, backupProvider, synchronizer, dataFolder):
          self.logger = logger
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

    def runBackup(self, inputFolder, outputFolder, excludePatterns, updateEvery) :
        raise Exception('not implemented')
   
    def isExcluded(self, path, excludePatterns):
        for pattern in excludePatterns:
            if fnmatch.fnmatch(path, pattern):
                return 1
        return 0
    
    def runRestore(self, backupFoler, outputFolder) :
        raise Exception('not implemented')
        
    def listFiles(self, settingsFile):
        raise Exception('not implemented')