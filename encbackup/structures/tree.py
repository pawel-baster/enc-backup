'''
Created on 21-04-2013

@author: pb
'''

class TreeNode(object):
    def __init__(self, path, lastModified, size):
        self.path = path
        self.lastModified = lastModified
        self.size = size
                
    def __eq__(self, other):
        return self.path == other.path and self.lastModified == other.lastModified and self.size == other.size
    
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
                        listOfTheirs.extend(other.files[j].getAllFiles())
                    
                    j = j + 1
                elif j >= len(other.files) or (i < len(self.files) and self.files[i].path < other.files[j].path):
                    print("Added %s to listOfOurs" % self.files[i].path)
                    if (isinstance(other.files[j], TreeNodeFile)):
                        listOfOurs.append(self.files[i])
                    else:
                        listOfOurs.extend(self.files[i].getAllFiles())
                    i = i + 1
                else: 
                    print("Deep comparing %s with %s" % (self.files[i].path, other.files[j].path))
                    if isinstance(self.files[i], TreeNodeDirectory) and isinstance(other.files[j], TreeNodeDirectory):
                        if (self.files[i].size != other.files[j].size 
                                or self.files[i].lastModified != other.files[j].lastModified
                                or self.files[i].numberOfFiles != other.files[j].numberOfFiles):
                            (theirs, ours, modified) = self.files[i].compare(other.files[j])
                            listOfTheirs.extend(theirs)
                            listOfOurs.extend(ours)
                            listOfModified.extend(modified)
                    elif isinstance(self.files[i], TreeNodeFile) and isinstance(other.files[j], TreeNodeFile):
                        if self.files[i].size != other.files[j].size or self.files[i].lastModified != other.files[j].lastModified:
                            listOfModified.append(self.files[i])                            
                    elif isinstance(self.files[i], TreeNodeDirectory) and isinstance(other.files[j], TreeNodeFile):
                        listOfOurs.extend(self.files[i].getAllFiles())
                        listOfTheirs.append(other.files[j])
                    elif isinstance(self.files[i], TreeNodeFile) and isinstance(other.files[j], TreeNodeDirectory):
                        listOfOurs.append(self.files[i])
                        listOfTheirs.extend(other.files[j].getAllFiles())
                                    
                    i = i + 1
                    j = j + 1
        else:
            print "nodes are identical, skipping recursion"
        
        return (listOfTheirs, listOfOurs, listOfModified)
        
    def getAllFiles(self):
        files = []
        for fileobj in self.files:
            if isinstance(fileobj, TreeNodeFile):
                files.append(fileobj)
            else:
                files = files.extend(fileobj.getAllFiles())
        return files
    
    def __str__(self):
        string = "Directory: %s (modified: %d, size: %d, number of children: %d) Files:" % (self.path, self.lastModified, self.size, self.numberOfFiles)
        for f in self.files:
            string = string + "\n" + str(f)
        return string

class TreeNodeFile(TreeNode):
    def __str__(self):
        return "File: %s (modified: %d, size: %d)" % (self.path, self.lastModified, self.size)
