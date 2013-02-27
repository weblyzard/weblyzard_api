'''
Created on Jan 4, 2013

@author: Albert Weichselbraun <albert.weichselbraun@htwchur.ch>
'''

from eWRT.ws.rest import RESTClient
from unittest import main, TestCase

POS_URL = "http://voyager.srv.weblyzard.net/ws"

class POS(RESTClient):
    '''
    POS Web Service
    '''
    
    def __init__(self, url=POS_URL, usr=None, pwd=None):
        RESTClient.__init__(self, url, usr, pwd)

    def pos_tagging(self, text, lang):
        """ tags the following text using the given language dictionary 
        @return: the corresponding ANNIE compatible annotations
        """
        return self.execute("pos-tagging", None, { 'text': text, 'lang': lang })


class POSTest(TestCase):
    
    def test_POS(self):
        p = POS()
        print p.pos_tagging('Guten Tag Herr Mayer!', 'de')
        

if __name__ == '__main__':
    main()
