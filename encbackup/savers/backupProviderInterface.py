'''
Created on 04-05-2012

@author: pawel
'''

class BackupProviderInterface(object):
    '''
    classdocs
    '''
    
    def backup(self, srcName, dstName) :
        raise Exception('Not implemented')
        
    def restore(self, srcName, dstName) :
        raise Exception('Not implemented')