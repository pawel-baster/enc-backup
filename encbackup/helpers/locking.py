'''
Created on Apr 24, 2013

@author: pb
'''

import os
import glob
import datetime

class SimpleLock:
    def __init__(self, lockDirectory):
        self.lockFileName = os.path.join(lockDirectory, datetime.datetime.today().strftime('%Y%m%d.lock'))
    
    def acquireLock(self):        
        if os.path.exists(self.lockFileName):
            return True
        else:
            # create an empty file
            open(self.lockFileName, 'w').close()
            return False

    def releaseLock(self):
        for filename in glob.glob(os.path.join(os.path.dirname(self.lockFileName), '*.lock')) :
            os.remove( filename )

if __name__ == '__main__':
    pass