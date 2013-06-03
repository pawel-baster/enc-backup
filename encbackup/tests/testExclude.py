'''
Created on 05-05-2012

@author: pawel
'''
import unittest
from helpers.filenameMatcher import FilenameMatcher

class ExcludeTest(unittest.TestCase):

    def testExclude(self):
        excludePatterns = ['*~', '*.bak' , '*.old', '*/cache/*', '*/Cache/*', '*/.metadata/*',
                           '/home/pawel/dev/python/.metadata/.plugins/*']
        cases = {
            '/tmp/file' : False,
            '/tmp/file.bak' : True,
            '/home/pawel/.mozilla/firefox/58l7zwm5.default/Cache/E/CD/5BFABd01' : True,
            '/home/pawel/.google/picasa/3.0/drive_c/Documents and Settings/pawel/Ustawienia lokalne/Dane aplikacji/Google/Picasa2/cache/cacheindex_lastfetch.pmp' : True,
            '/home/pawel/dev/python/.metadata/.plugins/com.python.pydev.analysis/python_v1_3tswbhuj9gc4kibexhrzgzdx/v1_indexcache/twisted.test.test_iutils_1q40.v1_indexcache' : True,
            '/home/pawel/dev/python/encbackup/encbackup/synchronizers/__init__.py' : False,
            '/home/pawel/Obrazy/2011/Dania/Skagen/IMG_0093.JPG' : False,
            '/home/pb/synced/dev/python/.metadata/.plugins/com.python.pydev.analysis/python_v1_3tswbhuj9gc4kibexhrzgzdx/v1_indexcache/gi.overrides.Dee_5bit.v1_indexcache' : True
        }
        for case, isExcluded in cases.items():
            self.assertEquals(isExcluded, FilenameMatcher.match(case, excludePatterns), 'file ' + case + ' is not filtered correctly')



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()