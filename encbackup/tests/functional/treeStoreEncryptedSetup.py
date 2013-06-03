'''
Created on 05-05-2012

BasicBackupController + NumberNameManager + EncryptedBackupProvider

@author: pawel
'''
import unittest
from abstractBackupRestoreScenario import AbstractBackupRestoreScenario

from controllers.treeStoreBackupController import TreeStoreBackupController
from names.hexNumbersNameManager import HexNumbersNameManager
from savers.encryptedBackupProvider import EncryptedBackupProvider
from helpers.serialize import PickleSerializer
from helpers.locking import SimpleLock


class TreeStoreEncryptedSetupTest(AbstractBackupRestoreScenario, unittest.TestCase):

    def _getInstance(self, logger, dataFolder, storeFolder, passphrase):
        return TreeStoreBackupController(
            dataFolder,
            SimpleLock(dataFolder),
            PickleSerializer(),
            HexNumbersNameManager(), 
            EncryptedBackupProvider(storeFolder, passphrase))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()