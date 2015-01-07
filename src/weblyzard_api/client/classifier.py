'''
Created on Jan 16, 2013

.. codeauthor: Albert Weichselbraun <albert.weichselbraun@htwchur.ch>
.. codeauthor: Norman Suesstrunk <norman.suesstrunk@htwchur.ch>
.. codeauthor: Philipp Kuntschik <philipp.kuntschik@htwchur.ch>
'''
import unittest

from eWRT.ws.rest import  MultiRESTClient
from weblyzard_api.client import WEBLYZARD_API_URL, WEBLYZARD_API_USER, WEBLYZARD_API_PASS
from sys import argv

class Classifier(MultiRESTClient):
    '''
    **Classifier**

    Provides support for text classification.
    '''
    CLASSIFIER_WS_BASE_PATH = '/joseph/rest/'

    def __init__(self, url=WEBLYZARD_API_URL,
                 usr=WEBLYZARD_API_USER, pwd=WEBLYZARD_API_PASS):
        '''
        :param url: URL of the jeremia web service
        :param usr: optional user name
        :param pwd: optional password
        '''
        MultiRESTClient.__init__(self, service_urls=url, user=usr, password=pwd)


    def hello_world(self):
        '''
        Simple hello world test.
        '''
        return self.request(self.CLASSIFIER_WS_BASE_PATH + 'helloworld')


    def classify(self, classifier_profile, weblyzard_xml, search_agents=None,
            num_results=1):
        '''
        Classify weblyzard XML documents based on the given classifier profile.

        :param classifier_profile: the profile to use for classification \
            (e.g. 'COMET', 'MK')
        :param weblyzard_xml: weblyzard_xml representation of the document to \
            classify
        :param search_agents: an optional list of search agents \
            (e.g. ``[1,2,3]``)
        :param num_results: number of classes to return
        :returns: the classification result
        '''
        classifier_request = {'xml_document': weblyzard_xml,
                              'numOfResults': num_results, }
        if search_agents is not None:
            classifier_request['searchAgents'] = search_agents

        classification_list = self.request(self.CLASSIFIER_WS_BASE_PATH
            + 'classify/' + classifier_profile, classifier_request)
        return {entry['searchagent']: entry['classification']
                for entry in classification_list}


    def train(self, classifier_profile, weblyzard_xml, correct_category,
            incorrect_category=None, document_timestamp=None):
        '''
        Trains (and corrects) the classifier's knowledge base.

        :param classifier_profile: the profile to use for classification \
            (e.g. 'COMET', 'MK')
        :param weblyzard_xml: weblyzard_xml representation of the document \
            to learn
        :param correct_category: the correct category for the document
        :param incorrect_category: optional information on the incorrect \
            category returned for this document
        :param document_timestamp: an optional timestamp, specifying when \
            the document has been classified (used for retraining temporal \
            knowledge bases)
        :returns: a response object with a status code and message.
        '''
        learn_request = {
            'xml_document': weblyzard_xml,
            'category': correct_category,
        }
        if incorrect_category is not None:
            learn_request['oldCategory'] = incorrect_category
            request_type = 'retrain/'
        else:
            request_type = 'learn/'

        if document_timestamp is not None:
            learn_request['documentTimeStamp'] = document_timestamp

        return self.request(self.CLASSIFIER_WS_BASE_PATH
            + request_type + classifier_profile, learn_request)


class TestClassifier(unittest.TestCase):

    WEBLYZARD_XML = """<?xml version="1.0" encoding="UTF-8"?>
                        <wl:page xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:wl="http://www.weblyzard.com/wl/2013#" wl:id="1001" dc:format="text/html" xml:lang="en">
                           <wl:title>Hello "world" more </wl:title>
                           <wl:body>Get in touch with Fast Track via email or Facebook. And follow us on Pinterest.1001</wl:body>
                           <wl:sentence wl:id="26d2d0113429b0dc98352c2b5fd842a1" wl:pos="1:UH -1:' 3:NN 1:' 1:RBR " wl:token="0,5 6,7 7,12 12,13 14,18" wl:is_title="true" wl:sem_orient="0.0" wl:significance="0.0"><![CDATA[Hello "world" more]]></wl:sentence>
                           <wl:sentence wl:id="7082ae05193c64ba5defe5e54ed15b98" wl:pos="-1:VB 0:IN 1:NN 2:IN 5:JJ 3:NNP 0:IN 6:NN 7:CC 8:NNP 0:. " wl:token="0,3 4,6 7,12 13,17 18,22 23,28 29,32 33,38 39,41 42,50 50,51" wl:sem_orient="0.0" wl:significance="0.0"><![CDATA[Get in touch with Fast Track via email or Facebook.]]></wl:sentence>
                           <wl:sentence wl:id="e5adef7b4beb1fd4c8edd26ba1d2825c" wl:pos="1:CC -1:VB 1:PRP 1:IN 3:NNP 1:CD " wl:token="0,3 4,10 11,13 14,16 17,26 26,31" wl:sem_orient="0.0" wl:significance="0.0"><![CDATA[And follow us on Pinterest.1001]]></wl:sentence>
                           <wl:content>Hello "world" more
                        Get in touch with Fast Track via email or Facebook. And follow us on Pinterest.1001</wl:content>
                        </wl:page>"""

    def test_submit_classify(self):
        ''' tests the basic submit routine '''
        classifier = Classifier()
        search_agents = [1, 2, 3]
        num_results = 3

        # call the web service
        result = classifier.classify('COMET', weblyzard_xml=self.WEBLYZARD_XML,
                search_agents=search_agents, num_results=num_results)

        # every search_agent should be covered in the result
        assert result.keys() == search_agents

        # for every search_agent are 'num_results' classes returned
        for _search_agent, classes in result.items():
            assert len(classes) == num_results

        print result


if __name__ == '__main__':
    if len(argv) == 1:
        unittest.main()
    else:
        from json import load
        fname = argv[1]
        with open(fname) as f:
            j = load(f)

        print Classifier().classify('COMET', weblyzard_xml=j['xml_document'],
            search_agents=j['searchAgents'], num_results=j['numOfResults'])

