'''
Created on 04-05-2012

@author: pawel

TODO: move mapping to different file so that it needn't be loaded to check if backup is necessary
TODO: when mirroring save last successful mirror time 
'''

class ControllerInterface(object):

    def runBackup(self, inputFolder, outputFolder, excludePatterns, updateEvery) :
        raise Exception('not implemented')
    
    def runRestore(self, backupFoler, outputFolder) :
        raise Exception('not implemented')
        
    def listFiles(self, settingsFile):
        raise Exception('not implemented')
