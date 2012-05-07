'''
Created on 2012-01-11

@author: pawel
'''

import shutil
import os
from backupProviderInterface import BackupProviderInterface

class PlainBackupProvider(BackupProviderInterface):
  
    def __init__(self, logger, backupFolder):
        self.backupFolder = backupFolder
        self.logger = logger
  
    def backup(self, src, dstName) :
        dst = os.path.join(self.backupFolder, dstName)  
        shutil.copyfile(src, dst)
        self.logger.log('Copied {src} to {dst}'.format(src=src, dst=dst))
    
    def restore(self, srcName, dst):
        src = os.path.join(self.backupFolder, srcName)
        shutil.copyfile(os.path.join(self.backupFolder, src), dst)
        self.logger.log('Restored {src} to {dst}'.format(src=src, dst=dst))
