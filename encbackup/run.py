#!/usr/bin/env python
'''
Created on 2012-01-11

@author: pawel
'''

import sys

from controllers.treeStoreBackupController import TreeStoreBackupController
#from names.subDirNumberNameManager import SubDirNumberNameManager2
#from savers.encryptedBackupProvider import EncryptedBackupProvider
#from synchronizers.lftpSynchronizer import LftpSynchronizer
from helpers.serialize import PickleSerializer
from helpers.locking import SimpleLock
import config

if __name__ == '__main__':
     
    try:          
            
        if len(sys.argv) < 2:
            print 'expected at least one command line argument (e.g. backup, restore or ls)'
            sys.exit()     
         
        if sys.argv[1] == 'backup' :
            #backup = BasicBackupController(
            #    logger,
            #    SubDirNumberNameManager2(),
            #    EncryptedBackupProvider(logger, config.storeBackupFolder, config.passphrasePath),
            #    LftpSynchronizer(logger, config.mirrorTo, config.storeBackupFolder, config.ftpSslVerification),
            #    config.dataPath)
            #config.excludePatterns.append(config.storeBackupFolder);        
            #backup.runBackup(config.foldersToBackup, config.storeBackupFolder, config.excludePatterns, config.updateBackupEvery)
            lock = SimpleLock(config.dataPath)
            serializer = PickleSerializer()
            backupProvide = TreeStoreBackupController(config.dataPath, lock, serializer)
            backupProvide.runBackup(config.foldersToBackup, config.storeBackupFolder, config.excludePatterns, config.updateBackupEvery)
    
        elif sys.argv[1] == 'ls' :
            raise Exception('requires refactoring')
            #backup = BasicBackupController(
            #    logger,
            #    SubDirNumberNameManager(), 
            #    EncryptedBackupProvider(logger, config.storeBackupFolder, config.passphrasePath),
            #    LftpSynchronizer(logger, config.mirrorTo, config.storeBackupFolder),
            #    config.updateBackupEvery,
            #    config.dataPath)
            # backup.listFiles(config.settingsPath)
        elif sys.argv[1] == 'restore' :
            if len(sys.argv) == 5:
                #backup = BasicBackupController(
                #    logger,
                #    SubDirNumberNameManager2(), 
                #    EncryptedBackupProvider(logger, sys.argv[2], sys.argv[4]),
                #    LftpSynchronizer(logger, '', ''),
                #    '/tmp')
                #backup.runRestore(sys.argv[2], sys.argv[3])
                pass
            else:
                print 'you need to specify input and output folder and passphrase file path for restore'
        else:  
            print 'unknown command line option (expected backup or ls)'
    except KeyboardInterrupt:
        Logger.log('Action aborted by a user')
    