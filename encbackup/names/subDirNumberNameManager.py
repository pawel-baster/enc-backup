'''
Created on 2012-01-11

@author: pawel
'''

import os
import time
import math

from numberNameManager import NumberNameManager

class SubDirNumberNameManager(NumberNameManager):
    '''
    uses two first digits as file name
    '''
    
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
    
class SubDirNumberNameManager2(NumberNameManager):
    '''
    uses two last digits as file name
    '''
    
    def encodeName(self, path, settings):
        now = int(time.time())  
        if path not in settings['mapping']:
            settings['lastId'] = settings['lastId'] + 1
            filename = hex(settings['lastId'])
            if len(filename) < 4:
                directory = '0' + filename[-1:]
            else:
                directory = filename[-2:]                 
            settings['mapping'][path] = {
                'filename' : os.path.join(directory, filename),
                'nextCheck' : now + int(24*3600*(1 + 90/math.ceil(float(os.path.getsize(path)+1)/100000)))
            }
                
        return settings['mapping'][path]['filename']