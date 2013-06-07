'''
Created on Apr 9, 2013

@author: pb
'''

import os
import time

from abstractBackupController import AbstractBackupController
from helpers.logging import Logger
from structures.tree import TreeNodeDirectory, TreeNodeFile

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
    
    def backupFolders(self, state, inputFolders, outputFolder, excludePatterns, stats):
        totalNumberOfFiles = 0
        totalSize = 0                
        for folder in inputFolders:
            Logger.log("Listing files in %s" % folder)
            tree = TreeNodeDirectory.createTreeFromFilesystem(folder, os.path.basename(folder), excludePatterns)
            if folder in state.trees:
                state.trees[folder].ensureDstPathOnAll()
                Logger.log("Comparing files in %s" % folder)
                (listOfRemoved, listOfAdded, listOfModified) = tree.merge(state.trees[folder])
            else:
                Logger.log("Adding all files from new folder %s" % folder)
                listOfAdded = tree.getAllFiles()
                listOfRemoved = []
                listOfModified = []
                
            upFolder = os.path.dirname(folder)    
                
            for f in listOfAdded:
                self.addFile(upFolder, f, state, stats)
                if f.dstPath is None: raise Exception('error')
                            
            for f in listOfModified:
                self.updateFile(upFolder, f, stats)
                if f.dstPath is None: raise Exception('error')
                
            for f in listOfRemoved:
                self.removeFile(upFolder, f, stats)
                if f.dstPath is None: raise Exception('error')
                
            tree.ensureDstPathOnAll()
            state.trees[folder] = tree
            totalNumberOfFiles += tree.numberOfFiles
            totalSize += tree.size
            
        state.lastCheck = int(time.time())            
        Logger.log("folder %s:" % folder)
        Logger.log("Number of files: %d, size: %.2f MB" % (totalNumberOfFiles, totalSize/1024/1024))     
       
    def addFile(self, folder, f, state, stats):
        Logger.log("Updating or adding file: %s" % f.path)
        stats.addedFilesSize += f.size
        stats.addedFilesCount += 1
        f.dstPath = self.nameManager.encodeName(f.path, state)
        self.backupProvider.backup(os.path.join(folder, f.path), f.dstPath)        
        
    def updateFile(self, folder, f, stats):
        assert f.dstPath is not None, "missing dstPath for updated file: " + str(f)
        Logger.log("Updating or adding file: %s" % f.path)
        stats.updatedFilesSize += f.size
        stats.updatedFilesCount += 1
        self.backupProvider.backup(os.path.join(folder, f.path), f.dstPath)
        
    def removeFile(self, folder, f, stats):
        assert f.dstPath is not None, "missing dstPath for removed file: " + str(f)
        Logger.log("Removing file: %s" % f.path)
        stats.removedFilesSize += f.size
        stats.removedFilesCount += 1
        self.backupProvider.remove(f.dstPath)
    
    def printStats(self, stats):
        Logger.log("Added %d files (%.2f MB)" % (stats.addedFilesCount, stats.addedFilesSize/1024/1024))
        Logger.log("Updated %d files (%.2f MB)" % (stats.updatedFilesCount, stats.updatedFilesSize/1024/1024))
        Logger.log("Removed %d files (%.2f MB)" % (stats.removedFilesCount, stats.removedFilesSize/1024/1024))
        
    def restoreFolders(self, state, backupFolder, outputFolder):
        for tree in state.trees.values():
            self.restoreFolder(tree, backupFolder, outputFolder)
            
    def restoreFolder(self, tree, backupFolder, outputFolder):
        for node in tree.files:
            if isinstance(node, TreeNodeFile):
                backupFileName = os.path.join(backupFolder, node.dstPath)
                restoredFileName = os.path.join(outputFolder, node.path)
                self.backupProvider.restore(backupFileName, restoredFileName)
                os.utime(restoredFileName, (node.lastModified, node.lastModified))
            elif isinstance(node, TreeNodeDirectory):
                self.restoreFolder(node, backupFolder, outputFolder)
            else:
                raise Exception('Unexpected node type')
            