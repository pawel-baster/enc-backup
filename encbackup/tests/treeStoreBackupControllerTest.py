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
    pass

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()