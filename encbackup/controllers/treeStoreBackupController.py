'''
Created on Apr 9, 2013

@author: pb
'''

import os
import time

from abstractBackupController import AbstractBackupController
from helpers.logging import Logger
from structures.tree import TreeNodeDirectory

class State:
    pass

class TreeStoreBackupController(AbstractBackupController):
    '''
    A backup controller that stores a tree of TreeNode objects 
    and compares it with the file system to prepare a list 
    of what has been added, removed or modified 
    '''
    
    def __init__(self, dataFolder, lock, serializer):
        AbstractBackupController.__init__(self, lock)
        self.treeFilePath = os.path.join(dataFolder, 'tree.dat')
        self.serializer = serializer

    def loadState(self):
        if os.path.exists(self.treeFilePath) :
            Logger.log("Reading state from %s" % self.treeFilePath)
            return self.serializer.unserialize(self.treeFilePath)
        else :
            Logger.log("Creating new state object")
            default = State()
            default.lastCheck = 0
            default.trees = {}
            return default 
    
    def saveState(self, state):
        Logger.log("Serializing state to %s" % self.treeFilePath)
        self.serializer.serialize(self.treeFilePath, state)
        #self.backupProvider.backup(filepath, backupName)             
        
    def isUpdatePending(self, state, updateEvery):
        return state.lastCheck + updateEvery < int(time.time())
    
    def backupFolder(self, state, inputFolders, outputFolder, excludePatterns, stats):                
        for folder in inputFolders:
            Logger.log("Listing files in %s" % folder)
            tree = TreeNodeDirectory.createTreeFromFilesystem(folder, os.path.basename(folder), excludePatterns)
            if folder in state.trees:
                (listOfRemoved, listOfAdded, listOfModified) = tree.compare(state.trees[folder])
            else:
                listOfAdded = tree.getAllFiles()
                listOfRemoved = []
                listOfModified = []
                
            for f in listOfAdded:
                self.backupFile(f, stats)
            
            for f in listOfModified:
                self.backupFile(f, stats)
                
            for f in listOfRemoved:
                self.removeFile(f, stats)
                
            state.trees[folder] = tree                   
       
    def backupFile(self, f, stats):
        Logger.log("Updating or adding file: %s" % f.path)
        #dstName = self.nameManager.encodeName(f.path, state.mapping)
        #self.backupProvider.backup(f.path, dstName)
        stats.archivedFilesSize += f.size
        stats.archivedFilesCount += 1
        
    def removeFile(self, f, stats):
        Logger.log("Removing file: %s" % f.path)
        #backupPath = os.path.join(self.backupProvider.getBackupFolder(), self.nameManager.encodeName(path, mapping))
        #os.remove(backupPath)
        #del state.mapping['mapping'][path]
        stats.removedFilesSize += f.size
        stats.removedFilesCount += 1    
    
    def printStats(self, stats):
        pass