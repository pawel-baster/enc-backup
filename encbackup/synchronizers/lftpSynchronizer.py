'''
Created on 2012-04-01

@author: pawel
'''
import datetime
import subprocess
import time
from synchronizerInterface import SynchronizerInterface

class LftpSynchronizer(SynchronizerInterface):

    def __init__(self, logger, targets, backupFolder, sslVerification=True):
        self.logger = logger
        self.targets = targets
        self.backupFolder = backupFolder
        self.sslVerification = sslVerification

    def synchronize(self, settings):
        for name, target in self.targets.items():
            if name not in settings['synchronized']:
                if name in settings['lastSynchronized']:
                    self.logger.log('Last successful synchronization of ' + name + ' at ' + datetime.datetime.fromtimestamp(settings['lastSynchronized'][name]).strftime('%Y-%m-%d %H:%M:%S'))
                else:
                    self.logger.log('Could not determine last successful synchronization time of ' + name + ' (perhaps never?)')                
                    
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
    
                if not self.sslVerification:
                    script = "set ssl:verify-certificate no\n" + script
    
                p = subprocess.Popen('lftp', stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                result = p.communicate(script)
                if result[0]: self.logger.log(result[0])
                if result[1]: self.logger.log('error: ' + result[1]) 
                if p.returncode == 0:
                    self.logger.log('OK')
                    settings['synchronized'][name] = int(time.time())
                    settings['lastSynchronized'][name] = int(time.time())
                else:
                    self.logger.log('synchronization failed for ' + name)
            else:
                self.logger.log('synchronization for ' + name + ' already performed')
