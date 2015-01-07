'''
Part-of-speech (POS) tagging service

.. codeauthor:: Albert Weichselbraun <albert.weichselbraun@htwchur.ch>
'''
import unittest
from eWRT.ws.rest import RESTClient

POS_URL = "http://voyager.srv.weblyzard.net/ws"

class POS(RESTClient):
    
    def __init__(self, url=POS_URL, usr=None, pwd=None):
        '''
        :param url: URL of the jeremia web service
        :param usr: optional user name
        :param pwd: optional password
        '''
        RESTClient.__init__(self, url, usr, pwd)

    def pos_tagging(self, text, lang):
        """ tags the following text using the given language dictionary 

        :returns: the corresponding ANNIE compatible annotations
        """
        return self.execute("pos-tagging", None, { 'text': text, 'lang': lang })


class POSTest(unittest.TestCase):
    
    def test_POS(self):
        p = POS()
        print p.pos_tagging('Guten Tag Herr Mayer!', 'de')
        

if __name__ == '__main__':
    unittest.main()
