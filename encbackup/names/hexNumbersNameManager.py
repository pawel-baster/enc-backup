'''
Created on 2012-01-11

@author: pawel
'''

from names.nameManagerInterface import NameManagerInterface
import os

class HexNumbersNameManager(NameManagerInterface):
    
    def encodeName(self, path, state):
        state.lastFileId += 1
        filename = hex(state.lastFileId)
        if len(filename) < 4:
            directory = '0' + filename[-1:]
        else:
            directory = filename[-2:]                 
        return os.path.join(directory, filename)
    