'''
Created on 2012-04-01

@author: pawel
'''
import subprocess
import time
from synchronizerInterface import SynchronizerInterface

class LftpSynchronizer(SynchronizerInterface):

    def __init__(self, logger, targets, backupFolder):
        self.logger = logger
        self.targets = targets
        self.backupFolder = backupFolder

    def synchronize(self, settings):
        for name, target in self.targets.items():
            if name not in settings['synchronized']:
                self.logger.log('connecting to ' + name)
                script = """set connection-limit 1
                    set net:max-retries 1
                    set cmd:fail-exit yes
                    set dns:fatal-timeout 60
                    echo connecting...                
                    open {target}
                    echo synchronizing...
                    mirror -R -e -v {outputFolder}
                    echo done.
                    \n\n""".format(target=target, outputFolder=self.backupFolder)
    
                p = subprocess.Popen('lftp', stdin=subprocess.PIPE)
                p.communicate(script)
                if p.returncode == 0:
                    self.logger.log('OK')
                    settings['synchronized'][name] = int(time.time())
                    settings['lastSynchronized'][name] = int(time.time())
                else:
                    self.logger.log('synchronization failed for ' + name)
            else:
                self.logger.log('synchronization for ' + name + ' already performed')
