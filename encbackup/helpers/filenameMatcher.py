'''
Created on Apr 22, 2013

@author: pb
'''

import fnmatch

class FilenameMatcher(object):
    '''
    classdocs
    '''

    @staticmethod
    def match(path, excludePatterns):
        for pattern in excludePatterns:
            if fnmatch.fnmatch(path, pattern):
                return 1
        return 0
