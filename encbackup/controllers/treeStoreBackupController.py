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
    
    def _createTree(self, root, name, excludePatterns):
        tree = TreeNodeDirectory(name, 0, 0, 0, [])
        for filename in sorted(os.listdir(root)):
            path = os.path.join(root, filename)
            if not self.isExcluded(path, excludePatterns):
                if os.path.isdir(path):
                    try:
                        if not os.path.islink(path):
                            node = self._createTree(path, name + os.path.sep + filename, excludePatterns)
                            if node.numberOfFiles > 0:
                                tree.size = tree.size + node.size
                                tree.lastModified = max(tree.lastModified, node.lastModified)
                                tree.numberOfFiles = tree.numberOfFiles + node.numberOfFiles
                                tree.files.append(node)
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
                        if size > 0:
                            lastModified = os.path.getmtime(path)
                            node = TreeNodeFile(name + os.path.sep + filename, lastModified, size)
                            tree.files.append(node)
                            tree.size = tree.size + size
                            tree.lastModified = max(tree.lastModified, lastModified)
                            tree.numberOfFiles = tree.numberOfFiles + 1
                    except IOError, e:
                        self.logger.log('could not save: ' + path + ': %s' % e)
                        self._errors.append('could not encrypt ' + path + ': %s' % e )
                else:
                    self.logger.log('skipping strange file: {0}'.format(path))
            else:
                self.logger.log('ignoring: ' + path)
         
        return tree
   
    def isExcluded(self, path, excludePatterns):
        for pattern in excludePatterns:
            if fnmatch.fnmatch(path, pattern):
                return 1
        return 0
    
    def runRestore(self, backupFoler, outputFolder) :
        raise Exception('not implemented')
        
    def listFiles(self, settingsFile):
        raise Exception('not implemented')