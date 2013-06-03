'''
Created on 05-05-2012

BasicBackupController + SubDirNumberNameManager + EncryptedBackupProvider

@author: pawel
'''
import unittest
from abstractBackupRestoreScenario import AbstractBackupRestoreScenario, MockSynchronizer

from encbackup.names.subDirNumberNameManager import SubDirNumberNameManager
from encbackup.controllers.basicBackupController import BasicBackupController
from encbackup.savers.encryptedBackupProvider import EncryptedBackupProvider

class Setup2Test(AbstractBackupRestoreScenario, unittest.TestCase):
    
    def _getInstance(self, logger, dataFolder, storeFolder, passphrase):
        return BasicBackupController(
            logger,
            SubDirNumberNameManager(), 
            EncryptedBackupProvider(logger, dataFolder, passphrase),
            MockSynchronizer(),
            storeFolder)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()