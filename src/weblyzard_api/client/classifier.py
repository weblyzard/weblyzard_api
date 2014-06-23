'''
Created on Jan 16, 2013

@author: Norman Suesstrunk <norman.suesstrunk@htwchur.ch>
'''
import unittest 

from eWRT.ws.rest import  MultiRESTClient
from weblyzard_api.client import WEBLYZARD_API_URL, WEBLYZARD_API_USER, WEBLYZARD_API_PASS

class Classifier(MultiRESTClient):
    
    '''
    base bath to the deployed seasonal classifier web project
    '''
    CLASSIFIER_WS_BASE_PATH = 'seasonalclassifier/rest/'
    
    def __init__(self, url=WEBLYZARD_API_URL, 
                 usr=WEBLYZARD_API_USER, pwd=WEBLYZARD_API_PASS):
        MultiRESTClient.__init__(self, service_urls=url, user=usr, password=pwd)

    def hello_world(self):
        '''
        tests the simple hello world service
        '''
        return self.request('seasonalclassifier/rest/helloworld') #hardcoded at the moment
    
    

class TestClassifier(unittest.TestCase):        
            
    def test_hello_world(self):
        classifier = Classifier()
        result = classifier.hello_world()
        assert result['helloWorld'] == 'hello world'
        

if __name__ == '__main__':
    unittest.main()
