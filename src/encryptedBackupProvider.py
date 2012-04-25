'''
Created on 2012-01-11

@author: pawel
'''

import os
import subprocess
import shlex 

class EncryptedBackupProvider:
  
    def __init__(self, logger, backupFolder, passphrasePath):
        self.logger = logger
        self.backupFolder = backupFolder
        self.passphrasePath = passphrasePath
  
    def getBackupFolder(self):
        return self.backupFolder
  
    def backup(self, srcName, dstName) :
        # TODO: remove os-specific /
        dst = self.backupFolder + os.path.sep + dstName
        fd=os.open(self.passphrasePath, os.O_RDONLY)
        cmd='gpg --no-tty --passphrase-fd {fd} -c'.format(fd=fd)
        with open(srcName, 'r') as stdin_fh:
            with open(dst, 'w') as stdout_fh:        
                proc=subprocess.Popen(shlex.split(cmd), stdin=stdin_fh, stdout=stdout_fh)        
                proc.communicate()
                if proc.returncode != 0:
                    raise Exception('gpg error code {0}'.format(proc.returncode))
        os.close(fd)
        self.logger.log('+ Encrypted {src} and saved as {dst}'.format(src=srcName, dst=dst))
  
    def restore(self, src, dst) :
        fd=os.open(self.passphrasePath, os.O_RDONLY)
        cmd='gpg --no-tty --passphrase-fd {fd}'.format(fd=fd)
        with open(self.backupFolder + os.path.sep + src, 'r') as stdin_fh:
            with open(dst, 'w') as stdout_fh:        
                proc=subprocess.Popen(shlex.split(cmd), stdin=stdin_fh, stdout=stdout_fh)        
                proc.communicate()
        os.close(fd)  
        self.logger.log('Decrypted {src} and saved as {dst}'.format(src=src, dst=dst))