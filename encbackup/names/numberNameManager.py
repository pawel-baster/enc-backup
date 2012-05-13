'''
Created on 2012-01-11

@author: pawel
'''

import os
import time
import math

from nameManagerInterface import NameManagerInterface

class NumberNameManager(NameManagerInterface):
    
    def encodeName(self, path, mapping):
        now = int(time.time())  
        if path not in mapping:
            mapping['lastId'] = mapping['lastId'] + 1
            mapping['mapping'][path] = {
                'filename' : hex(mapping['lastId']),
                'nextCheck' : now + int(24*3600*(1 + 90/math.ceil(float(os.path.getsize(path)+1)/100000)))
            }
                
        return mapping['mapping'][path]['filename']

    def decodeName(self, name, settings):
        for path in settings['mapping']:
            if path['filename'] == name:
                return path 
        
        raise Exception('missing mapping for name: ' + name)
        
    def getCount(self, settings):
        return len(settings['mapping'])