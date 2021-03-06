'''
Created on 21-04-2013

@author: pb
'''

import os

from helpers.filenameMatcher import FilenameMatcher

class TreeNode(object):
    def __init__(self, path, lastModified, size, dstPath = None):
        self.path = path
        self.lastModified = lastModified
        self.size = size
        self.dstPath = dstPath
                
    def __eq__(self, other):
        if not isinstance(other, TreeNode):
            return False
        return self.path == other.path and self.lastModified == other.lastModified and self.size == other.size
    
    @staticmethod
    def createTreeFromFilesystem(root, name, excludePatterns):
        tree = TreeNodeDirectory(name, 0, 0, 0, [])
        for filename in sorted(os.listdir(root)):
            path = os.path.join(root, filename)
            if not FilenameMatcher.match(path, excludePatterns):
                if os.path.isdir(path):
#                    try:
                        if not os.path.islink(path):
                            node = TreeNodeDirectory.createTreeFromFilesystem(path, name + os.path.sep + filename, excludePatterns)
                            if node.numberOfFiles > 0:
                                tree.size = tree.size + node.size
                                tree.lastModified = max(tree.lastModified, node.lastModified)
                                tree.numberOfFiles = tree.numberOfFiles + node.numberOfFiles
                                tree.files.append(node)
#                        else:
#                            self.logger.log('skipping symbolic link ' + path)
#                            self._errors.append('skipping symbolic link ' + path)
 #                   except IOError, e:
#                        self.logger.log('could not enter directory: ' + path + ':')
#                        self.logger.log('> %s' % e)
 #                       self._errors.append('could not enter directory: ' + path + ': %s' % e)
                elif os.path.isfile(path):
       #             try:
                        size = os.path.getsize(path)
                        if size > 0:
                            lastModified = os.path.getmtime(path)
                            node = TreeNodeFile(name + os.path.sep + filename, lastModified, size)
                            tree.files.append(node)
                            tree.size = tree.size + size
                            tree.lastModified = max(tree.lastModified, lastModified)
                            tree.numberOfFiles = tree.numberOfFiles + 1
                    #except IOError, e:
  #                      self.logger.log('could not save: ' + path + ': %s' % e)
  #                      self._errors.append('could not encrypt ' + path + ': %s' % e )
   #             else:
   #                 self.logger.log('skipping strange file: {0}'.format(path))
   #         else:
   #             self.logger.log('ignoring: ' + path)
         
        return tree
    
class TreeNodeDirectory(TreeNode):
    def __init__(self, path, lastModified, size, numberOfFiles, files):
        TreeNode.__init__(self, path, lastModified, size)
        self.files = files
        self.numberOfFiles = numberOfFiles
        
    def __eq__(self, other):
        if not isinstance(other, TreeNodeDirectory):
            return False
        return TreeNode.__eq__(self, other) and self.numberOfFiles == other.numberOfFiles and self.files == other.files

    def merge(self, other):
        '''
        creates lists of what should be added, removed or updated
        '''
        listOfOurs = []
        listOfTheirs = []
        listOfModified = []     
        #print str(other)
        
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
                        listOfTheirs.extend(other.files[j].getAllFiles())
                    
                    j = j + 1
                elif j >= len(other.files) or (i < len(self.files) and self.files[i].path < other.files[j].path):
                    print("Added %s to listOfOurs" % self.files[i].path)
                    if (isinstance(self.files[i], TreeNodeFile)):
                        listOfOurs.append(self.files[i])
                    else:
                        listOfOurs.extend(self.files[i].getAllFiles())
                    i = i + 1
                else: 
                    print("Deep comparing %s with %s" % (self.files[i].path, other.files[j].path))
                    if isinstance(self.files[i], TreeNodeDirectory) and isinstance(other.files[j], TreeNodeDirectory):
                        #directory compare
                        if (self.files[i].size != other.files[j].size 
                                or self.files[i].lastModified != other.files[j].lastModified
                                or self.files[i].numberOfFiles != other.files[j].numberOfFiles):
                            (theirs, ours, modified) = self.files[i].merge(other.files[j])
                            listOfTheirs.extend(theirs)
                            listOfOurs.extend(ours)
                            listOfModified.extend(modified)
                        else:
                            self.files[i] = other.files[j]
                    elif isinstance(self.files[i], TreeNodeFile) and isinstance(other.files[j], TreeNodeFile):
                        # modified file
                        if self.files[i].size != other.files[j].size or self.files[i].lastModified != other.files[j].lastModified:                            
                            listOfModified.append(self.files[i])                            
                        self.files[i].dstPath = other.files[j].dstPath
                    elif isinstance(self.files[i], TreeNodeDirectory) and isinstance(other.files[j], TreeNodeFile):
                        # directory -> file
                        listOfOurs.extend(self.files[i].getAllFiles())
                        listOfTheirs.append(other.files[j])
                    elif isinstance(self.files[i], TreeNodeFile) and isinstance(other.files[j], TreeNodeDirectory):
						# file -> directory
                        listOfOurs.append(self.files[i])
                        listOfTheirs.extend(other.files[j].getAllFiles())
                                    
                    i = i + 1
                    j = j + 1
        else:
            print "nodes are identical, skipping recursion"
            self.files = other.files
            
        print 'listOfModified:'
        for item in listOfModified:
            print str(item)
            
        print 'listOfOurs:'
        for item in listOfOurs:
            print str(item)
            
        print 'listOfTheirs:'
        for item in listOfTheirs:
            print str(item) 
        
        return (listOfTheirs, listOfOurs, listOfModified)
    
    def ensureDstPathOnAll(self):
        for node in self.files:
            if isinstance(node, TreeNodeFile):
                assert node.dstPath is not None, "ensureDstPathOnAll(): missing dstPath on file: " + str(node)
            else:
                node.ensureDstPathOnAll()
            
        
    def getAllFiles(self):
        files = []
        for fileobj in self.files:
            if isinstance(fileobj, TreeNodeFile):
                files.append(fileobj)
            else:
                files.extend(fileobj.getAllFiles())
        return files
    
    def __str__(self):
        string = "Directory: %s (modified: %d, size: %d, number of children: %d) Files:" % (self.path, self.lastModified, self.size, self.numberOfFiles)
        for f in self.files:
            string = string + "\n" + f.printRecursively()
        return string
    
    def printRecursively(self, indent=0):
        string = ' ' * indent + "Directory: %s (modified: %d, size: %d, number of children: %d) Files:" % (self.path, self.lastModified, self.size, self.numberOfFiles)
        for f in self.files:
            string = string + "\n" + f.printRecursively(indent + 2)
        return string

class TreeNodeFile(TreeNode):
    def __str__(self):
        return "File: %s (modified: %d, size: %d, encypted path: %s)" % (self.path, self.lastModified, self.size, self.dstPath if hasattr(self, 'dstPath') else 'n/a')
    
    def printRecursively(self, indent=0):
        return ' ' * indent + str(self)
