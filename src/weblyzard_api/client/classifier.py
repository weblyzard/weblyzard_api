# -*- coding: utf8 -*-
'''
Created on Jan 16, 2013

.. codeauthor: Albert Weichselbraun <albert.weichselbraun@htwchur.ch>
.. codeauthor: Norman Suesstrunk <norman.suesstrunk@htwchur.ch>
.. codeauthor: Philipp Kuntschik <philipp.kuntschik@htwchur.ch>

'''
import unittest

from eWRT.ws.rest import  MultiRESTClient
from eWRT.util.module_path import get_resource
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

    def classify_v2(self, classifier_profile, weblyzard_xml, search_agents=None,
            num_results=1):
        '''
        Classify weblyzard XML documents based on the given classifier profile
        using the new classifier interface

        :param classifier_profile: the profile to use for classification \
            (e.g. 'COMET', 'MK')
        :param weblyzard_xml: weblyzard_xml representation of the document to \
            classify
        :param search_agents: a list of search agent dictionaries which are \
            composed as follows
           {
            {"name":"Axa Winterthur",
             "id":9,
             "product_list":[
                {"name":"AXA WINTERTHUR VERS. PRODUKTE RP","id":300682},
                {"name":"AXA WINTERTHUR FINANZ PERSONEN RP","id":300803},
                {"name":"AXA WINTERTHUR FINANZ PRODUKTE RP","id":300804},
             ] 
            }
           ]
        :param num_results: number of classes to return
        :returns: the classification result
        '''
        classifier_request = {'xml_document': weblyzard_xml,
                              'numOfResults': num_results, }
        if search_agents is not None:
            classifier_request['searchAgents'] = search_agents

        classification_list = self.request(self.CLASSIFIER_WS_BASE_PATH
            + '2/classify/' + classifier_profile, classifier_request)
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

    get_search_agent_ids = staticmethod(lambda search_agents: [sa['id']
                                                  for sa in search_agents])

    def test_submit_classify_v2(self):
        ''' test the version 2 classifier '''

        weblyzard_xml = open(get_resource(__file__, 'data/classifier_v2_testfile.xml')).read()

        classifier = Classifier()
        search_agents = [
            {
            "name": "Santésuisse", "id": 412,
            "product_list":[
                   {"name":"SANTESUISSE FINANZ ENGAGEMENT RP", "id": 327432},
                   {"name":"SANTESUISSE FINANZ ENTWICKLUNG RP", "id": 327435},
                   {"name":"SANTESUISSE FINANZ PERSONEN RP", "id": 327442},
                   {"name":"SANTESUISSE FINANZ PRODUKTE RP", "id": 327444},
                   {"name":"SANTESUISSE FINANZ REGULATION RP", "id": 327446},
                   {"name":"SANTESUISSE FINANZ RESEARCH RP", "id": 327452},
                   {"name":"SANTESUISSE VERS. ALLGEMEIN RP", "id": 327562},
                   {"name":"SANTESUISSE VERS. ENGAGEMENT RP", "id": 327564},
                   {"name":"SANTESUISSE VERS. ENTWICKLUNG RP", "id": 327566},
                   {"name":"SANTESUISSE VERS. PERSONEN RP", "id": 327568},
                   {"name":"SANTESUISSE VERS. PRODUKTE RP", "id": 327570},
                   {"name":"SANTESUISSE VERS. REGULATION RP", "id": 327572},
                   {"name":"SANTESUISSE VERS. RESEARCH RP", "id": 327574},
                   {"name":"SANTESUISSE FINANZ ALLGEMEIN RP", "id": 327428}
                ]},
                {
                "name": "Krankenkassen", "id":460,
                "product_list":[
                   {"name":"KRANKENKASSEN FINANZ ENGAGEMENT RP", "id": 342053},
                   {"name":"KRANKENKASSEN FINANZ ENTWICKLUNG RP", "id": 342055},
                   {"name":"KRANKENKASSEN FINANZ PERSONEN RP", "id": 342056},
                   {"name":"KRANKENKASSEN FINANZ PRODUKTE RP", "id": 342057},
                   {"name":"KRANKENKASSEN FINANZ REGULATION RP", "id": 342058},
                   {"name":"KRANKENKASSEN FINANZ RESEARCH RP", "id": 342059},
                   {"name":"KRANKENKASSEN VERS. ALLGEMEIN RP", "id": 342060},
                   {"name":"KRANKENKASSEN VERS. ENGAGEMENT RP", "id": 342061},
                   {"name":"KRANKENKASSEN VERS. ENTWICKLUNG RP", "id": 342062},
                   {"name":"KRANKENKASSEN VERS. PERSONEN RP", "id": 342063},
                   {"name":"KRANKENKASSEN VERS. PRODUKTE RP", "id": 342064},
                   {"name":"KRANKENKASSEN VERS. REGULATION RP", "id": 342065},
                   {"name":"KRANKENKASSEN VERS. RESEARCH RP", "id": 342066},
                   {"name":"KRANKENKASSEN FINANZ ALLGEMEIN RP", "id": 342052}
                ]}
        ] 
        num_results = 3

        # call the web service
        result = classifier.classify_v2('COMET', weblyzard_xml=weblyzard_xml,
                search_agents=search_agents, num_results=num_results)

        # every search_agent should be covered in the result
        assert set(result.keys()) == set(self.get_search_agent_ids(search_agents))

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

        print Classifier().classify_v2('COMET', weblyzard_xml=j['xml_document'],
            search_agents=j['searchAgents'], num_results=j['numOfResults'])

