'''
Created on 2012-01-11

@author: pawel
'''

import sys

from basicBackupJob import BasicBackupJob
from numberNameManager import NumberNameManager
from encryptedBackupProvider import EncryptedBackupProvider
from lftpMirror import LftpMirror
from simpleLogger import SimpleLogger
import config

if __name__ == '__main__':
     
    logger = SimpleLogger() 
        
    if len(sys.argv) < 2:
        print 'expected at least one command line argument (e.g. backup, restore or ls)'
        sys.exit()     
     
    if sys.argv[1] == 'backup' :
        backup = BasicBackupJob(
            logger,
            NumberNameManager(),
            EncryptedBackupProvider(logger, config.storeBackupFolder, config.passphrasePath),
            LftpMirror(logger, config.mirrorTo, config.storeBackupFolder),
            config.updateBackupEvery,
            config.dataPath)
        config.excludePatterns.append(config.storeBackupFolder);        
        backup.runBackup(config.folderToBackup, config.excludePatterns, config.settingsPath)
    elif sys.argv[1] == 'ls' :
        backup = BasicBackupJob(
            logger,
            NumberNameManager(), 
            EncryptedBackupProvider(logger, config.storeBackupFolder, config.passphrasePath),
            LftpMirror(logger, config.mirrorTo, config.storeBackupFolder),
            config.updateBackupEvery,
            config.dataPath)
        backup.listFiles(config.settingsPath)
    elif sys.argv[1] == 'restore' :
        if len(sys.argv) == 5:
            backup = BasicBackupJob(
                logger,
                NumberNameManager(), 
                EncryptedBackupProvider(logger, sys.argv[2], sys.argv[4]),
                LftpMirror(logger, '', ''),
                0,
                '/tmp')
            backup.runRestore(sys.argv[3])
        else:
            print 'you need to specify input and output folder and passphrase file path for restore'
    else:  
        print 'unknown command line option (expected backup or ls)'
    