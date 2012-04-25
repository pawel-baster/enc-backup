'''
Created on 2012-01-11

@author: pawel
'''

import shutil

class PlainBackupProvider:
  
    def __init__(self, backupFolder):
        self.backupFolder = backupFolder
  
    def backup(self, src, dstName) :
        dst = '{0}{1}'.format(self.backupFolder, dstName)  
        shutil.copyfile(src, dst)
        print 'Copied {src} to {dst}'.format(src=src, dst=dst)
    
    def restore(self, src, dst):
        shutil.copyfile(src, dst)
