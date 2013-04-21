'''
Created on Apr 9, 2013

@author: pb
'''
import unittest
from subprocess import call
import os

from encbackup.controllers.treeStoreBackupController import TreeStoreBackupController
from encbackup.controllers.treeStoreBackupController import TreeNodeDirectory
from encbackup.controllers.treeStoreBackupController import TreeNodeFile
from encbackup.names.numberNameManager import NumberNameManager
from encbackup.simpleLogger import SimpleLogger

class MockSynchronizer:
    def synchronize(self, settings):
        pass
    
class MockBackupProvider:
        
    def backup(self, srcName, dstName) :
        raise Exception('Not implemented')
        
    def restore(self, srcName, dstName) :
        raise Exception('Not implemented')

class TreeStoreBackupControllerTest(unittest.TestCase):

    def compareTrees(self, expected, actual):
        assert expected.path == actual.path, "asserting that expected '%s' equals '%s'" % (expected.path, actual.path)
        assert expected.size == actual.size, "asserting that expected %d equals %d for file %s" % (expected.size, actual.size, actual.name)
        assert expected.lastModified == actual.lastModified, "asserting that expected %d equals %d" % (expected.lastModified, actual.lastModified)
        assert expected.__class__.__name__ == actual.__class__.__name__
        if isinstance(expected, TreeNodeDirectory):
            assert len(expected.files) == len(actual.files)
            for (node1, node2) in zip(expected.files, actual.files):
                self.compareTrees(node1, node2)

    def setUp(self):
        logger = SimpleLogger()
        self.instance = TreeStoreBackupController(logger,
            NumberNameManager(), 
            MockBackupProvider(),
            MockSynchronizer(),
            'test')
        
    def testCreateTree(self):
        self.root = os.path.join(os.path.dirname( __file__ ), 'fixtures', self.__class__.__name__)
        result = self.instance._createTree(self.root, 'root', ['*_ignored'])
        expectedResult = self.generateTree()
        #reset timestamps to 1970-01-01 00:01, time-zone sensitive for now
        print("find '%s' -exec touch -t 197001010001 {} \;" % self.root)
        call("find '%s' -exec touch -t 197001010101 {} \;" % self.root, shell=True)

        print("expected result:")
        print(expectedResult)
        print("actual result:")
        print(result)
        self.compareTrees(expectedResult, result)

    def testCompareNodes(self):
        backup = TreeNodeDirectory("root", 1, 1, 5, [
           TreeNodeDirectory("root/modified", 1, 1, 3, [
              TreeNodeFile("root/modified/modified.txt", 1, 1),
              TreeNodeFile("root/modified/size_changed.txt", 1, 1),
              TreeNodeFile("root/modified/untoched.txt", 1, 1)              
           ]),
           TreeNodeDirectory("root/not_changed", 1, 1, 1, [
              TreeNodeFile("root/not_changed/same.txt", 1, 1)
           ]),
           TreeNodeDirectory("root/removed", 1, 1, 1, [
              TreeNodeFile("root/removed/removed.txt", 1, 1)
           ]),           
        ])
        
        live = TreeNodeDirectory("root", 1, 2, 5, [
           TreeNodeDirectory("root/added", 1, 2, 2, [
              TreeNodeFile("root/added/added.txt", 1, 2),
           ]),
           TreeNodeDirectory("root/modified", 1, 2, 3, [              
              TreeNodeFile("root/modified/modified.txt", 2, 1),
              TreeNodeFile("root/modified/size_changed.txt", 1, 2),
              TreeNodeFile("root/modified/untoched.txt", 1, 1)
           ]),
           TreeNodeDirectory("root/not_changed", 1, 1, 1, [
              TreeNodeFile("root/not_changed/same.txt", 1, 1)
           ]),                      
        ])
        
        expectedListOfRemoved = ['root/removed/removed.txt']
        expectedListOfAdded = ['root/added/added.txt']
        expectedListOfModified = ['root/modified/modified.txt', 'root/modified/size_changed.txt']
        
        (listOfRemoved, listOfAdded, listOfModified) = live.compare(backup)
        extractNameCallback = lambda node: node.path
        assert expectedListOfRemoved == map(extractNameCallback, listOfRemoved), str(expectedListOfRemoved) + " does not equal " + str(map(extractNameCallback, listOfRemoved))
        assert expectedListOfAdded == map(extractNameCallback, listOfAdded), str(expectedListOfAdded) + " does not equal " + str(map(extractNameCallback, listOfAdded))
        assert expectedListOfModified == map(extractNameCallback, listOfModified), str(expectedListOfModified) + " does not equal " + str(map(extractNameCallback, listOfModified))

    def generateTree(self):
        tree = TreeNodeDirectory("root", 60, 8, 2, [
            TreeNodeFile('root/file1.txt', 60, 4),
            TreeNodeDirectory('root/folder1', 60, 4, 1, [
                TreeNodeFile('root/folder1/file3.txt', 60, 4)
            ])           
        ])
        return tree

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()