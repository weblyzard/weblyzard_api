'''
Created on Jan 16, 2013

@author: Norman Suesstrunk <norman.suesstrunk@htwchur.ch>
'''
import unittest 

from eWRT.ws.rest import  MultiRESTClient
from weblyzard_api.client.jeremia import Jeremia
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
    
    DOCS = [ {'id': content_id,
              'body': 'Get in touch with Fast Track via email or Facebook. And follow us on Pinterest.' + str(content_id),
              'title': 'Hello "world" more ',
              'format': 'text/html',
              'header': {}}  for content_id in xrange(1000,1020)]
    
            
    def test_submit_classify(self):
        
        
        # 1. step: send document to jeremia and retrieve the weblyzard document
        j = Jeremia()
        print 'submitting document...'
        document_annotated = j.submit_document(self.DOCS[1])
        self.assertTrue(document_annotated != "")
        
        type(document_annotated['xml_content'])
        #print document_annotated['xml_content']
        
        json_classify_data= {
                'searchAgents': [1, 2, 3],
                'numOfResults': 3, 
                'xml_document': document_annotated['xml_content']
        }
        
        
        # 2. step: send processed document to the classifier
        classifier = Classifier()
        result = classifier.classify(json_classify_data)
        print result         
        self.assertTrue(result is not None)

if __name__ == '__main__':
    unittest.main()
