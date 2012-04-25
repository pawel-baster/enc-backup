'''
Created on 2012-04-01

@author: pawel
'''

import datetime

class SimpleLogger(object):

    def log(self, msg):
        print datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S :'), msg
    