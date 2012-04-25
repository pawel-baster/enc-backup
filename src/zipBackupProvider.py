'''
Created on 2012-01-11

@author: pawel
'''

import zlib

class ZipBackupProvider:
  
    def __init__(self, backupFolder):
        self.backupFolder = backupFolder
  
    def backup(self, srcName, dstName):
        dst = '{0}{1}'.format(self.backupFolder, dstName)  
        source= file( srcName, "r" )
        compObj= zlib.compressobj()
        dest= file( dst, "w" )
        block= source.read( 2048 )
        while block:
            cBlock= compObj.compress( block )
            dest.write(cBlock)
            block= source.read( 2048 )
        cBlock= compObj.flush()
        dest.write( cBlock )
        source.close()
        dest.close()
    
    def restore(self, srcName, dstName):
        dst = '{0}{1}'.format(self.backupFolder, dstName)  
        source= file( srcName, "r" )
        compObj= zlib.compressobj()
        dest= file( dst, "w" )
        block= source.read( 2048 )
        while block:
            cBlock= compObj.compress( block )
            dest.write(cBlock)
            block= source.read( 2048 )
        cBlock= compObj.flush()
        dest.write( cBlock )
        source.close()
        dest.close()