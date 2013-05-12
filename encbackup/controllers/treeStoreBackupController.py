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
    
    def __init__(self, dataFolder, lock, serializer, nameManager, backupProvider):
        AbstractBackupController.__init__(self, lock, nameManager, backupProvider)
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
            default.lastFileId = 0
            default.trees = {}
            default.treeFilePathEncoded = self.nameManager.encodeName(self.treeFilePath, default)
            return default 
    
    def saveState(self, state):
        Logger.log("Serializing state to %s" % self.treeFilePath)
        self.serializer.serialize(self.treeFilePath, state)
        self.backupProvider.backup(self.treeFilePath, state.treeFilePathEncoded)             
        
    def isUpdatePending(self, state, updateEvery):
        return state.lastCheck + updateEvery < int(time.time())
    
    def backupFolder(self, state, inputFolders, outputFolder, excludePatterns, stats):                
        for folder in inputFolders:
            Logger.log("Listing files in %s" % folder)
            tree = TreeNodeDirectory.createTreeFromFilesystem(folder, os.path.basename(folder), excludePatterns)
            if folder in state.trees:
                Logger.log("Comparing files in %s" % folder)
                (listOfRemoved, listOfAdded, listOfModified) = tree.compare(state.trees[folder])
            else:
                Logger.log("Adding all files from new folder %s" % folder)
                listOfAdded = tree.getAllFiles()
                listOfRemoved = []
                listOfModified = []
                
            upFolder = os.path.dirname(folder)    
                
            for f in listOfAdded:
                self.addFile(upFolder, f, state, stats)
                            
            for f in listOfModified:
                self.updateFile(upFolder, f, stats)
                
            for f in listOfRemoved:
                self.removeFile(upFolder, f, stats)
                
            state.trees[folder] = tree
            Logger.log("folder %s:" % folder)
            Logger.log("Number of files: %d, size: %.2f MB" % (tree.numberOfFiles, tree.size/1024/1024))                   
       
    def addFile(self, folder, f, state, stats):
        Logger.log("Updating or adding file: %s" % f.path)
        stats.addedFilesSize += f.size
        stats.addedFilesCount += 1
        f.dstPath = self.nameManager.encodeName(f.path, state)
        self.backupProvider.backup(os.path.join(folder, f.path), f.dstPath)        
        
    def updateFile(self, folder, f, stats):
        Logger.log("Updating or adding file: %s" % f.path)
        stats.updatedFilesSize += f.size
        stats.updatedFilesCount += 1
        self.backupProvider.backup(os.path.join(folder, f.path), f.dstPath)
        
    def removeFile(self, folder, f, stats):
        Logger.log("Removing file: %s" % f.path)
        stats.removedFilesSize += f.size
        stats.removedFilesCount += 1
        os.remove(f.dstPath)
    
    def printStats(self, stats):
        Logger.log("Added %d files (%.2f MB)" % (stats.addedFilesCount, stats.addedFilesSize/1024/1024))
        Logger.log("Updated %d files (%.2f MB)" % (stats.updatedFilesCount, stats.updatedFilesSize/1024/1024))
        Logger.log("Removed %d files (%.2f MB)" % (stats.removedFilesCount, stats.removedFilesSize/1024/1024))