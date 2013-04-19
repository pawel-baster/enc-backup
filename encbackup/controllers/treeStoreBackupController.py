'''
Created on Apr 9, 2013

@author: pb
'''

import fnmatch
import os

from controllerInterface import ControllerInterface

class TreeNode(object):
    def __init__(self, path, lastModified, size):
        self.path = path
        self.lastModified = lastModified
        self.size = size
                
    def __eq__(self, other):
        return self.path == other.path and self.lastModified == other.lastModified and self.size == other.size and self.numberOfChildren == other.numberOfChildren
    
class TreeNodeDirectory(TreeNode):
    def __init__(self, path, lastModified, size, numberOfFiles, files):
        TreeNode.__init__(self, path, lastModified, size)
        self.files = files
        self.numberOfFiles = numberOfFiles
        
    def __eq__(self, other):
        return TreeNode.__eq__(self, other) and self.numberOfFiles == other.numberOfFiles and self.files == other.files

    def compare(self, other):
        '''
        creates lists of what should be added, removed or updated
        '''
        listOfOurs = []
        listOfTheirs = []
        listOfModified = []     
        
        if self.path != self.path or self.lastModified != other.lastModified or self.size != other.size:
            print "going in..."
            i = 0
            j = 0
            while i < len(self.files) or j < len(other.files):
                if i < len(self.files) and j < len(other.files):
                    print("Comparing %s with %s" % (self.files[i].path, other.files[j].path))
                else: 
                    print("Comparing %d with %d" % (i, j))
                
                if i >= len(self.files) or (j < len(other.files) and self.files[i].path > other.files[j].path):
                    if (isinstance(other.files[j], TreeNodeFile)):
                        listOfTheirs.append(other.files[j])
                        print("Added %s to listOfTheirs" % other.files[j].path)
                    else:
                        raise Exception('not impl')
                        #listOfTheirs add recursively
                    
                    j = j + 1
                elif j >= len(other.files) or (i < len(self.files) and self.files[i].path < other.files[j].path):
                    print("Added %s to listOfOurs" % self.files[i].path)
                    listOfOurs.append(self.files[i])
                    i = i + 1
                else: 
                    print("Deep comparing %s with %s" % (self.files[i].path, other.files[j].path))
                    listOfModified.append(self.files[i])
                    i = i + 1
                    j = j + 1
        else:
            print "nodes are identical, skipping recursion"
        
        return (listOfTheirs, listOfOurs, listOfModified)
        
    def __str__(self):
        string = "Directory: %s (modified: %d, size: %d, number of children: %d) Files:" % (self.path, self.lastModified, self.size, self.numberOfFiles)
        for f in self.files:
            string = string + "\n" + str(f)
        return string

class TreeNodeFile(TreeNode):
    def __str__(self):
        return "File: %s (modified: %d, size: %d)" % (self.path, self.lastModified, self.size)

class TreeStoreBackupController(ControllerInterface):
    '''
    classdocs
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