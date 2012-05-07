'''
Created on 05-05-2012

BasicBackupController + SubDirNumberNameManager + PlainBackupProvider

@author: pawel
'''
import unittest
from abstractBackupRestoreScenario import AbstractBackupRestoreScenario

from encbackup.names.subDirNumberNameManager import SubDirNumberNameManager
from encbackup.controllers.basicBackupController import BasicBackupController
from encbackup.savers.plainBackupProvider import PlainBackupProvider

class Setup3Test(AbstractBackupRestoreScenario, unittest.TestCase):
    
    def _getInstance(self, logger, dataFolder, storeFolder, passphrase):
        return BasicBackupController(
            logger,
            SubDirNumberNameManager(), 
            PlainBackupProvider(logger, dataFolder),
            None,
            storeFolder)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()