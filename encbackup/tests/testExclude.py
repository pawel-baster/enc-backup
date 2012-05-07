'''
Created on 05-05-2012

@author: pawel
'''
import unittest
from encbackup.controllers.basicBackupController import BasicBackupController

class BasicControllerExcludeTest(unittest.TestCase):

    def setUp(self):        
        self.backup = BasicBackupController(None, None, None, None, '')

    def testExclude(self):
        excludePatterns = ['*~', '*.bak' , '*.old', '*/cache/*', '*/Cache/*']
        cases = {
            '/tmp/file' : False,
            '/tmp/file.bak' : True,
            '/home/pawel/.mozilla/firefox/58l7zwm5.default/Cache/E/CD/5BFABd01' : True,
            '/home/pawel/.google/picasa/3.0/drive_c/Documents and Settings/pawel/Ustawienia lokalne/Dane aplikacji/Google/Picasa2/cache/cacheindex_lastfetch.pmp' : True,
        }
        for case, isExcluded in cases.items():
            self.assertEquals(isExcluded, self.backup.isExcluded(case, excludePatterns), 'file ' + case + ' is not filtered correctly')



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()