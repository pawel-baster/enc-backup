'''
Created on 2012-01-30

@author: pawel
'''
import os
import shutil
import random
import base64
import filecmp

from encbackup.simpleLogger import SimpleLogger

class MockSynchronizer:
    def synchronize(self, settings):
        pass

class AbstractBackupRestoreScenario:

    def setUp(self):        
        self.root = os.path.join(os.path.dirname( __file__ ), 'fixtures', self.__class__.__name__)
        if (os.path.exists(self.root)):
            shutil.rmtree(self.root)
        os.mkdir(self.root)
        os.mkdir(os.path.join(self.root, 'data'))
        os.mkdir(os.path.join(self.root, 'backup'))
        os.mkdir(os.path.join(self.root, 'restore'))
        os.mkdir(os.path.join(self.root, 'store'))
        
        passphrase = self._createRandomFile(self.root, '_passphrase')
        logger = SimpleLogger() 
        self.backup = self._getInstance(logger, os.path.join(self.root, 'data'), os.path.join(self.root, 'store'), passphrase) 
   
    def _getInstance(self, logger, dataFolder, storeFolder, passphrase):
        raise Exception('Not implemented in this abstract class')
        
    def testScenario1(self):
        self._testBackup()
        self._testAdd()   
        self._testDelete()
        
               
    def _testBackup(self):
        print 'creating random structure and testing if all required files are restored'
        self._createDirStructure(os.path.join(self.root, 'backup'), 50)
        self._check()
    
    def _testAdd(self):
        print 'testing adding new file - if it will be included in next restore'
        os.mkdir(os.path.join(self.root, 'backup', 'new'))
        self._createRandomFile(os.path.join(self.root, 'backup', 'new'), '_new')
        # at this moment compare() should raise exception - it tests the unit test, not the actual working code
        try:
            self._compare();
            self.fail('added new file but not found while comparing')
        except Exception:
            # that's expected
            pass
      
        # perform backup and restore and check if they contain the same files    
        self._check()
        
    def _testDelete(self):
        print 'deleting a file'
        shutil.rmtree(os.path.join(self.root, 'backup', 'new'))
        mapping = self.backup._loadSettingsFile(self.backup.mappingFilePath + '_backup', None)
        self.backup.cleanup(['*_ignored'], mapping, True)        
        self._check()

    def _check(self):
        shutil.rmtree(os.path.join(self.root, 'restore'))
        os.mkdir(os.path.join(self.root, 'restore'))
        self.backup.runBackup([os.path.join(self.root, 'backup')], 
                              os.path.join(self.root, 'store'),
                               ['*_ignored'], 
                               0)
        #backup mapping file for later usage:
        shutil.copyfile(self.backup.mappingFilePath, self.backup.mappingFilePath + '_backup')
        self.backup.runRestore(os.path.join(self.root, 'data'),
                               os.path.join(self.root, 'restore'))
        self._compare();
        
    def _compareFilesContent(self, path1, path2):
        self.assertTrue(filecmp.cmp(path1, path2, False), 'files not identical: ' + path1 + ' and ' + path2)
    
    def _compare(self):
        comparator = filecmp.dircmp(os.path.join(self.root, 'backup'), 
                                    os.path.join(self.root, 'restore', self.root, 'backup'))
        comparator.report_full_closure()
        if len(comparator.right_only) != 0:
            print 'unexpected files: ', comparator.right_only
            self.fail('there are some files in restore folder that should not be there')
            
        for filename in comparator.left_only:
            if not filename.endswith('_ignored') and not filename.startswith('folder_'):
                print 'missing files: ', comparator.right_only
                self.fail('not ignored file or folder missing in restore: ' + filename)
        
    def _createDirStructure(self, root, counter):
        print 'going into ', root
        if not os.path.exists(root):
            os.mkdir(root)
            
        i = counter
        while i > 0:
            choice = random.randint(0,10)
            if choice == 0:
                itemsToCreate = random.randint(1, i)
                self._createDirStructure(os.path.join(root, 'folder_' + self._createRandomFileName()), itemsToCreate)
                i = i - itemsToCreate
                pass
            elif choice == 1:
                itemsToCreate = random.randint(1, i)
                self._createDirStructure(os.path.join(root, 'folder_' + self._createRandomFileName() + '_ignored'), itemsToCreate)
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
        name = os.path.join(folder, 'file_' + self._createRandomFileName() + suffix)
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