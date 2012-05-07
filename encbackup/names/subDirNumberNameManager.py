'''
Created on 2012-01-11

@author: pawel
'''

import os
import time
import math

from numberNameManager import NumberNameManager

class SubDirNumberNameManager(NumberNameManager):
    
    def encodeName(self, path, settings):
        now = int(time.time())  
        if path not in settings['mapping']:
            settings['lastId'] = settings['lastId'] + 1
            filename = hex(settings['lastId'])
            settings['mapping'][path] = {
                'filename' : os.path.join(filename[2:4], filename),
                'nextCheck' : now + int(24*3600*(1 + 90/math.ceil(float(os.path.getsize(path)+1)/100000)))
            }
                
        return settings['mapping'][path]['filename']