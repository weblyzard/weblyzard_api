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
    CLASSIFIER_WS_BASE_PATH = '/joseph/rest/'
    
    def __init__(self, url=WEBLYZARD_API_URL, 
                 usr=WEBLYZARD_API_USER, pwd=WEBLYZARD_API_PASS):
        MultiRESTClient.__init__(self, service_urls=url, user=usr, password=pwd)

    def hello_world(self):
        '''
        tests the simple hello world service
        '''
        return self.request(self.CLASSIFIER_WS_BASE_PATH + 'helloworld') #hardcoded at the moment
    
    def classify(self, classifier_profile, classifier_request):
        classification_list = self.request(self.CLASSIFIER_WS_BASE_PATH + 'classify', classifier_request)
        return {entry['searchagent']: entry['classification'] for entry in classification_list}
    
    

class TestClassifier(unittest.TestCase):
    
    DOCS = [ {'id': content_id,
              'body': 'Get in touch with Fast Track via email or Facebook. And follow us on Pinterest.' + str(content_id),
              'title': 'Hello "world" more ',
              'format': 'text/html',
              'header': {}}  for content_id in xrange(1000,1020)]
    
            
    def test_submit_classify(self):
        
        jeremia_xml_document = """<?xml version="1.0" encoding="UTF-8"?>
                <wl:page xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:wl="http://www.weblyzard.com/wl/2013#" wl:id="1001" dc:format="text/html" xml:lang="en">
                   <wl:title>Hello "world" more </wl:title>
                   <wl:body>Get in touch with Fast Track via email or Facebook. And follow us on Pinterest.1001</wl:body>
                   <wl:sentence wl:id="26d2d0113429b0dc98352c2b5fd842a1" wl:pos="1:UH -1:' 3:NN 1:' 1:RBR " wl:token="0,5 6,7 7,12 12,13 14,18" wl:is_title="true" wl:sem_orient="0.0" wl:significance="0.0"><![CDATA[Hello "world" more]]></wl:sentence>
                   <wl:sentence wl:id="7082ae05193c64ba5defe5e54ed15b98" wl:pos="-1:VB 0:IN 1:NN 2:IN 5:JJ 3:NNP 0:IN 6:NN 7:CC 8:NNP 0:. " wl:token="0,3 4,6 7,12 13,17 18,22 23,28 29,32 33,38 39,41 42,50 50,51" wl:sem_orient="0.0" wl:significance="0.0"><![CDATA[Get in touch with Fast Track via email or Facebook.]]></wl:sentence>
                   <wl:sentence wl:id="e5adef7b4beb1fd4c8edd26ba1d2825c" wl:pos="1:CC -1:VB 1:PRP 1:IN 3:NNP 1:CD " wl:token="0,3 4,10 11,13 14,16 17,26 26,31" wl:sem_orient="0.0" wl:significance="0.0"><![CDATA[And follow us on Pinterest.1001]]></wl:sentence>
                   <wl:content>Hello "world" more 
                Get in touch with Fast Track via email or Facebook. And follow us on Pinterest.1001</wl:content>
                </wl:page>"""
                        
        json_classify_data= {
                'searchAgents': [1, 2, 3],
                'numOfResults': 3, 
                'xml_document': jeremia_xml_document
        }
        
        
        # 2. step: send processed document to the classifier
        classifier = Classifier()
        result = classifier.classify('COMET', json_classify_data)
        print result         
        self.assertTrue(result is not None)

if __name__ == '__main__':
    unittest.main()
