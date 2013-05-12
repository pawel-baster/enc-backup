'''
Created on 2012-01-11

@author: pawel
'''

class NameManagerInterface:
    
    def encodeName( self, path, state ):
        raise NotImplementedError( "Should have implemented this" )
    