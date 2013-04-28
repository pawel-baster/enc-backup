'''
Created on 26-04-2013

@author: pb
'''

import pickle
import os
import shutil

class PickleSerializer(object):
    '''
    classdocs
    '''

    def unserialize(self, filepath):
        with open(filepath, 'r') as f:
            return pickle.load(f)
        
    def serialize(self, filepath, obj):
        if os.path.exists(filepath):
            shutil.copyfile(filepath, filepath + '.old')
        sfile = open(filepath, 'w')
        pickle.dump(obj, sfile)
        sfile.close()
