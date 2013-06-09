#!/usr/bin/env python
'''
Created on 2012-01-11

@author: pawel
'''

import sys
import os

from controllers.treeStoreBackupController import TreeStoreBackupController
from names.hexNumbersNameManager import HexNumbersNameManager
from savers.encryptedBackupProvider import EncryptedBackupProvider
from helpers.serialize import PickleSerializer
from helpers.locking import SimpleLock
from helpers.logging import Logger
import config


if __name__ == '__main__':
     
    lock = SimpleLock(config.dataPath) 
     
    try:          
            
        nameManager = HexNumbersNameManager()
        backupProvider = EncryptedBackupProvider(config.storeBackupFolder, config.passphrasePath)        
        serializer = PickleSerializer()
           
        if len(sys.argv) < 2:
            print 'expected at least one command line argument (e.g. backup, restore or ls)'
            sys.exit()     
         
        if sys.argv[1] == 'backup' :
            controller = TreeStoreBackupController(config.dataPath, lock, serializer, nameManager, backupProvider)
            controller.runBackup(config.foldersToBackup, config.storeBackupFolder, config.excludePatterns, config.updateBackupEvery)
        elif sys.argv[1] == 'ls' :
            state = serializer.unserialize(os.path.join(config.dataPath, 'tree.dat'))
            for tree in state.trees.values():
                for f in tree.getAllFiles():
                    print f.path
                      
        elif sys.argv[1] == 'restore' :
            if len(sys.argv) == 5:
                pass
            else:
                print 'you need to specify input and output folder and passphrase file path for restore'
        else:  
            print 'unknown command line option (expected backup or ls)'
    except KeyboardInterrupt:
        Logger.log('Action aborted by a user')
        lock.releaseLock()
    