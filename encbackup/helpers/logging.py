'''
Created on 2012-04-01

@author: pawel
'''

import datetime

class Logger(object):

    printDebug = True

    @staticmethod
    def _printLine(msg):
        print datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S :'), msg

    @staticmethod
    def log(msg):
        Logger._printLine(msg)
    
    @staticmethod    
    def debug(msg):
        if Logger.printDebug:
            Logger._printLine(msg)
    