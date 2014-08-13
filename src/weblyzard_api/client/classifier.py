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
    
    def classify(self, classifyRequest):
        return self.request('seasonalclassifier/rest/classify', classifyRequest)
    
    

class TestClassifier(unittest.TestCase):
    
    TEST_JSON_CLASSIFY_DATA = {
        'searchAgents': [1, 2, 3],
        'numOfResults': 3, 
        'document': 
            {
                'title': 'id', 
                'body': 'Get in touch with Fast Track via email or Facebook. And follow us on Pinterest.', 
                'sentence': [
                        {    
                        'id' : 'b78a3223503896721cca1303f776159b',
                        'token' : '0,5',
                        'is_title' : 'false',
                        'text' : 'Title',
                        'sem_orient' : '0.0',
                        'significance' : '0.0'
                        }, 
                        {
                        'id': '7082ae05193c64ba5defe5e54ed15b98',
                        'token' : '0,3 4,6 7,12 13,17 18,22 23,28 29,32 33,38 39,41 42,50 50,51',
                        'is_title' : 'true',
                        'text' : 'Get in touch with Fast Track via email or Facebook.',
                        'sem_orient' : '0.0',
                        'significance' : '0.0',
                        'pos' : '-1:VB 0:IN 1:NN 2:IN 5:JJ 3:NNP 0:IN 6:NN 7:CC 8:NNP 0:. '
                        }, 
                              
                    ]
                }
             }
            
    def test_submit_classify(self):
        classifier = Classifier()
        result = classifier.classify(self.TEST_JSON_CLASSIFY_DATA)
        self.assertTrue(result is not None)
        
        

if __name__ == '__main__':
    unittest.main()
