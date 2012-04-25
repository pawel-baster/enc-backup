'''
Created on 2012-01-11

@author: pawel
'''

import sys
import os

from alternativeBackupJob import AlternativeBackupJob
from numberNameManager import NumberNameManager
from encryptedBackupProvider import EncryptedBackupProvider
from lftpMirror import LftpMirror
from simpleLogger import SimpleLogger
import config


if __name__ == '__main__':
     
    logger = SimpleLogger() 
    backup = AlternativeBackupJob(
            logger,
            NumberNameManager(), 
            EncryptedBackupProvider(logger, config.storeBackupFolder, config.passphrasePath),
            LftpMirror(logger, config.mirrorTo, config.storeBackupFolder),
            config.updateBackupEvery,
            config.dataPath)
    
    if len(sys.argv) != 2:
        print 'expected one command line argument (backup or ls)'
        sys.exit()     
     
    if sys.argv[1] == 'backup' :
        config.excludePatterns.append(config.storeBackupFolder);        
        backup.runBackup(config.folderToBackup, config.excludePatterns, config.settingsPath)
    elif sys.argv[1] == 'ls' :
        backup.listFiles(config.settingsPath)
    else:  
        print 'unknown command line option (expected backup or ls)'
    