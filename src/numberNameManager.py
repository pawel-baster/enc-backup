'''
Created on 2012-01-11

@author: pawel
'''

import os
import time
import math

from nameManagerInterface import NameManagerInterface

class NumberNameManager (NameManagerInterface):
    
    def encodeName(self, path, settings):
        now = int(time.time())  
        if path not in settings['mapping']:
            settings['lastId'] = settings['lastId'] + 1
            settings['mapping'][path] = {
                'filename' : hex(settings['lastId']),
                'nextCheck' : now + int(24*3600*(1 + 90/math.ceil(float(os.path.getsize(path)+1)/100000)))
            }
                
        return settings['mapping'][path]['filename']

    def decodeName(self, name, settings):
        for path in settings['mapping']:
            if path['filename'] == name:
                return path 
        
        raise Exception('missing mapping for name: ' + name)
        
    def getCount(self, settings):
        return len(settings['mapping'])