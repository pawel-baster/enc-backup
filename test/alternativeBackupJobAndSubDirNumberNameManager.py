'''
Created on 2012-01-30

@author: pawel
'''
import unittest
import os
import shutil
import random
import base64
import filecmp

from src.subDirNumberNameManager import SubDirNumberNameManager
from src.basicBackupJob import BasicBackupJob
from src.encryptedBackupProvider import EncryptedBackupProvider
from src.simpleLogger import SimpleLogger
from src.lftpMirror import LftpMirror

class AlternativeBackupJobAndSubDirNumberNameManager(unittest.TestCase):

    def setUp(self):        
        self.root = os.path.dirname( __file__ )  + os.path.sep + 'fixtures' + os.path.sep + 'AlternativeBackupJobAndSubDirNumberNameManager' + os.path.sep
        if (os.path.exists(self.root)):
            shutil.rmtree(self.root)
        os.mkdir(self.root)
        os.mkdir(self.root + 'data')
        os.mkdir(self.root + 'backup')
        os.mkdir(self.root + 'restore')
        
        passphrase = self._createRandomFile(self.root, '_passphrase')
        logger = SimpleLogger() 
        self.backup = BasicBackupJob(
            logger,
            SubDirNumberNameManager(), 
            EncryptedBackupProvider(logger, self.root + 'data', passphrase),
            LftpMirror(logger, {}, ''),
            0,
            self.root)
   
    def testExclude(self):
        excludePatterns = ['*~', '*.bak' , '*.old', '*/cache/*', '*/Cache/*']
        cases = {
            '/tmp/file' : False,
            '/tmp/file.bak' : True,
            '/home/pawel/.mozilla/firefox/58l7zwm5.default/Cache/E/CD/5BFABd01' : True,
            '/home/pawel/.google/picasa/3.0/drive_c/Documents and Settings/pawel/Ustawienia lokalne/Dane aplikacji/Google/Picasa2/cache/cacheindex_lastfetch.pmp' : True,
        }
        for case, isExcluded in cases.items():
            if (isExcluded != self.backup.isExcluded(case, excludePatterns)):
                raise Exception('file ' + case + ' is not filtered correctly')

        
    def testScenario1(self):
        self._testBackup()
        self._testAdd()   
        self._testDelete()
        
               
    def _testBackup(self):
        print 'creating random structure and testing if all required files are restored'
        self._createDirStructure(self.root + 'backup/', 50)
        self._check()
    
    def _testAdd(self):
        print 'testing adding new file - if it will be included in next restore'
        os.mkdir(self.root + 'backup/new')
        self._createRandomFile(self.root + 'backup/new/', '_new')
        # at this moment compare() should raise exception - it tests the unit test, not the actual working code
        try:
            self._compare();
            ok = False
        except Exception:
            ok = True
            
        if not ok:
            raise Exception('added new file but not found while compating')
        
        # perform backup and restore and check if they contain the same files    
        self._check()
        
    def _testDelete(self):
        print 'deleting a file'
        shutil.rmtree(self.root + 'backup/new')
        self.backup.cleanup(['*_ignored'], self.root + 'settings', True)        
        self._check()

    def _check(self):
        shutil.rmtree(self.root + 'restore')
        os.mkdir(self.root + 'restore')
        self.backup.runBackup(self.root + 'backup', ['*_ignored'], self.root + 'settings')
        self.backup.runRestore(self.root + 'restore')
        self._compare();
        
    def _compareFilesContent(self, path1, path2):
        if not filecmp.cmp(path1, path2, False):
            raise Exception('files not identical: ' + path1 + ' and ' + path2)
    
    def _compare(self):
        comparator = filecmp.dircmp(self.root + 'backup', self.root + 'restore' + self.root + 'backup')
        comparator.report_full_closure()
        if len(comparator.right_only) != 0:
            print 'unexpected files: ', comparator.right_only
            raise Exception('there are some files in restore folder that should not be there')
            
        for filename in comparator.left_only:
            if not filename.endswith('_ignored') and not filename.startswith('folder_'):
                print 'missing files: ', comparator.right_only
                raise Exception('not ignored file or folder missing in restore: ' + filename)
        
    def _createDirStructure(self, root, counter):
        print 'going into ', root
        if not os.path.exists(root):
            os.mkdir(root)
            
        i = counter
        while i > 0:
            choice = random.randint(0,10)
            if choice == 0:
                itemsToCreate = random.randint(1, i)
                self._createDirStructure(root + 'folder_' + self._createRandomFileName() + '/', itemsToCreate)
                i = i - itemsToCreate
                pass
            elif choice == 1:
                itemsToCreate = random.randint(1, i)
                self._createDirStructure(root + 'folder_' + self._createRandomFileName() + '_ignored/', itemsToCreate)
                i = i - 1
                pass
            elif choice == 2:
                self._createRandomFile(root, '_ignored')
                i = i - 1
                pass
            else:
                self._createRandomFile(root, '')
                i = i - 1
                pass
            
    def _createRandomFile(self, folder, suffix):
        name = folder + 'file_' + self._createRandomFileName() + suffix
        print 'creating random file: ', name
        f = open(name, 'w' )
        f.write( self._createRandomContent() )
        f.close()
        return name

    def _createRandomFileName(self):
        #return base64.b64encode(os.urandom(3))
        return '{0}'.format(random.randint(10000, 99999))
    
    def _createRandomContent(self):
        return base64.b64encode(os.urandom(5))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()