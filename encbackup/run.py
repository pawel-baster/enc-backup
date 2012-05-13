'''
Created on 2012-01-11

@author: pawel
'''

import sys

from controllers.basicBackupController import BasicBackupController
from names.subDirNumberNameManager import SubDirNumberNameManager
from savers.encryptedBackupProvider import EncryptedBackupProvider
from synchronizers.lftpSynchronizer import LftpSynchronizer
from simpleLogger import SimpleLogger
import config

if __name__ == '__main__':
     
    logger = SimpleLogger() 
        
    if len(sys.argv) < 2:
        print 'expected at least one command line argument (e.g. backup, restore or ls)'
        sys.exit()     
     
    if sys.argv[1] == 'backup' :
        backup = BasicBackupController(
            logger,
            SubDirNumberNameManager(),
            EncryptedBackupProvider(logger, config.storeBackupFolder, config.passphrasePath),
            LftpSynchronizer(logger, config.mirrorTo, config.storeBackupFolder),
            config.dataPath)
        config.excludePatterns.append(config.storeBackupFolder);        
        backup.runBackup(config.foldersToBackup, config.storeBackupFolder, config.excludePatterns, config.updateBackupEvery)

    elif sys.argv[1] == 'ls' :
        raise Exception('requires refactoring')
        backup = BasicBackupController(
            logger,
            SubDirNumberNameManager(), 
            EncryptedBackupProvider(logger, config.storeBackupFolder, config.passphrasePath),
            LftpSynchronizer(logger, config.mirrorTo, config.storeBackupFolder),
            config.updateBackupEvery,
            config.dataPath)
       # backup.listFiles(config.settingsPath)
    elif sys.argv[1] == 'restore' :
        if len(sys.argv) == 5:
            backup = BasicBackupController(
                logger,
                SubDirNumberNameManager(), 
                EncryptedBackupProvider(logger, sys.argv[2], sys.argv[4]),
                LftpSynchronizer(logger, '', ''),
                0,
                '/tmp')
            backup.runRestore(sys.argv[3])
        else:
            print 'you need to specify input and output folder and passphrase file path for restore'
    else:  
        print 'unknown command line option (expected backup or ls)'
    