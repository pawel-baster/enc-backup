'''
Created on 2012-01-11

@author: pawel
'''

import os
import subprocess
import shlex 
from backupProviderInterface import BackupProviderInterface

class EncryptedBackupProvider(BackupProviderInterface):
  
    def __init__(self, logger, backupFolder, passphrasePath):
        self.logger = logger
        self.backupFolder = backupFolder
        self.passphrasePath = passphrasePath
        if not os.path.exists(passphrasePath):
            raise Exception('Could not find a file: ' + passphrasePath)
  
    def getBackupFolder(self):
        return self.backupFolder
  
    def backup(self, srcName, dstName) :
        try:
            # TODO: remove os-specific /
            fd=os.open(self.passphrasePath, os.O_RDONLY)
            dst = os.path.join(self.backupFolder, dstName)            
            cmd='gpg --no-tty --force-mdc --passphrase-fd {fd} -c'.format(fd=fd)
            self._createDirsForFile(dst)
            with open(srcName, 'r') as stdin_fh:
                with open(dst, 'w') as stdout_fh:        
                    proc=subprocess.Popen(shlex.split(cmd), stdin=stdin_fh, stdout=stdout_fh)        
                    proc.communicate()
                    if proc.returncode != 0:
                        raise IOError('gpg return code is non-zero ({code})'.format(code=proc.returncode))
            if (not os.path.exists(dst)) or (os.path.getsize(dst) == 0):
                raise IOError('File {src} was not encrypted properly as {dst}'.format(src=srcName, dst=dst))
        except:
            raise
        finally:
            os.close(fd)
        
        assert os.path.exists(dst) and os.path.getsize(dst) > 0, 'File {0} not saved correctly'.format(dst)
        self.logger.log('+ Encrypted {src} and saved as {dst}'.format(src=srcName, dst=dst))
  
    def restore(self, src, dst) :
        try:
            fd=os.open(self.passphrasePath, os.O_RDONLY)
            cmd='gpg --no-tty --passphrase-fd {fd}'.format(fd=fd)
            self._createDirsForFile(dst)
            with open(os.path.join(self.backupFolder, src), 'r') as stdin_fh:
                with open(dst, 'w') as stdout_fh:        
                    proc=subprocess.Popen(shlex.split(cmd), stdin=stdin_fh, stdout=stdout_fh)        
                    proc.communicate()
                    if proc.returncode != 0:
                        raise IOError('gpg return code is non-zero ({code})'.format(code=proc.returncode))
            if (not os.path.exists(dst)) or (os.path.getsize(dst) == 0):
                raise IOError('File {src} was not encrypted properly as {dst}'.format(src=src, dst=dst))
        except:
            raise
        finally:
            os.close(fd)  
        
        self.logger.log('Decrypted {src} and saved as {dst}'.format(src=src, dst=dst))
        
    def _createDirsForFile(self, filename):
        d = os.path.dirname(filename)
        if not os.path.exists(d):
            os.makedirs(d)

