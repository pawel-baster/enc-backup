'''
Created on 2012-01-11

@author: pawel
'''

class NameManagerInterface:
    
    def encodeName( self, path, settings ):
        raise NotImplementedError( "Should have implemented this" )
    
    def decodeName( self, path, settings ):
        raise NotImplementedError( "Should have implemented this" )
