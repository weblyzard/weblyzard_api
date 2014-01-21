#!/usr/bin/python
# -*- coding: utf8 -*-
'''
Created on Jan 4, 2013

moduleauthor:: Albert Weichselbraun <albert.weichselbraun@htwchur.ch>

New supported calls:
- recognize/focus?profiles=ofwi.people&profiles=ofwi.organizations.context
- recognize/searchXml/ofwi.people

'''
import unittest

from eWRT.access.http import Retrieve
from eWRT.ws.rest import MultiRESTClient

from weblyzard_api.xml_content import XMLContent
from weblyzard_api.client import (WEBLYZARD_API_URL, WEBLYZARD_API_USER, 
                                  WEBLYZARD_API_PASS)

INTERNAL_PROFILE_PREFIX = 'extras.'

class Recognize(MultiRESTClient):
    '''
    class:: Recognize 
    EntityLyzard/Recognize Web Service
    '''
    OUTPUT_FORMATS = ('standard', 'minimal', 'annie')    
    URL_PATH = 'recognize/rest/recognize'
    
    def __init__(self, url=WEBLYZARD_API_URL, 
                 usr=WEBLYZARD_API_USER, pwd=WEBLYZARD_API_PASS):
        MultiRESTClient.__init__(self, service_urls=url, user=usr, password=pwd)
    
    def list_profiles(self):
        ''' pre-loaded profiles
            e.g. [u'Cities.DACH.10000.de_en', u'People.DACH.de']
        '''
        return self.request('list_profiles')

    def list_configured_profiles(self):
        ''' profiles supported in the current configuration '''
        return self.request('list_configured_profiles')

    def add_profile(self, profile_name, force=False):
        ''' pre-loads the given profile '''
        is_internal_profile = profile_name.startswith(INTERNAL_PROFILE_PREFIX)
        profile_exists = profile_name in self.list_profiles() and not force
        
        if not is_internal_profile and not profile_exists:
            return self.request('add_profile/%s' % profile_name)

    def remove_profile(self, profile_name):
        ''' removes a profile from the list of pre-loaded profiles '''
        return self.request('remove_profile/%s' % profile_name)

    def search(self, profile_name, text, debug=False, max_entities=1, buckets=1, 
               limit=1, output_format='minimal'):
        '''
        :param profileName: the profile to search in
        :param text: the text to search in
        :param debug: compute and return an explanation
        :param buckets: only return n buckets of hits with the same score
        :param max_entities: number of results to return (removes the top hit's
                             tokens and rescores the result list subsequently
        :param limit: only return that many results
        :param output_format: the output format to use ('standard', 'minimal'*, 'annie')
        :rtype: the tagged text
        '''
        assert output_format in self.OUTPUT_FORMATS
        
        self.add_profile(profile_name)

        return self.request(path='search/%s' % profile_name, 
                            parameters=text, 
                            query_parameters={'rescore': max_entities, 
                                              'buckets': buckets, 
                                              'limit': limit, 
                                              'wt': output_format, 
                                              'debug': debug })

    def search_documents(self, profile_name, doc_list, debug=False, 
                         max_entities=1, buckets=1, limit=1, 
                         output_format='minimal'):
        '''
        :param profileName: the profile to search in
        :param doc_list: a list of documents to analyze in one of the 
                         following formats:
                         (a) dict: ( {'content_id': 12, 
                                      'content': u'the text to analyze'})
                         (b) weblyzardXML: ( XMLContent('<?xml version="1.0"...').as_list(),
                                             XMLContent('<?xml version="1.0"...').as_list(), )

        :param debug: compute and return an explanation
        :param buckets: only return n buckets of hits with the same score
        :param max_entities: number of results to return (removes the top hit's
                             tokens and rescores the result list subsequently
        :param limit: only return that many results
        :param output_format: the output format to use ('standard', 'minimal'*, 'annie')
        :rtype: the tagged dictionary
        '''
        assert output_format in self.OUTPUT_FORMATS
        if not doc_list:
            return 

        self.add_profile(profile_name)

        content_type = 'application/json'
        
        if 'content_id' in doc_list[0]:
            search_command = 'searchDocuments'
        elif 'id' in doc_list[0]:
            search_command = 'searchXmlDocuments'
        else:
            raise ValueError("Unsupported input format.")

        self.add_profile(profile_name)

        return self.request(path='%s/%s' % (search_command, profile_name), 
                            parameters=doc_list, 
                            content_type=content_type,
                            query_parameters={'rescore': max_entities, 
                                              'buckets': buckets, 
                                              'limit': limit, 
                                              'wt': output_format, 
                                              'debug': debug})
    
    def get_focus(self, profile_names, doc_list, max_results=1):
        ''' 
        Returns the focus and annotations of the given document 

        :param profile_names: a list of profile names
        :param doc_list: a list of documents to analyze based on the weblyzardXML format
        :param max_results: maximum number of results to include 

        query: recognize/focus?profiles=ofwi.people&profiles=ofwi.organizations.context
        '''
        assert (isinstance(profile_names, list) or isinstance(profile_names, tuple))
        
        if not doc_list:
            return
        elif 'id' not in doc_list[0]:
            raise ValueError('Unsupported input format.')

        # add missing profiles
        for profile_name in profile_names:
            self.add_profile(profile_name)

        return self.request(path='focusDocuments', 
                            parameters=doc_list, 
                            query_parameters={'profiles': profile_names, 
                                              'rescore': max_results, 
                                              'buckets': max_results, 
                                              'limit': max_results})

    def status(self):
        return self.request(path='status')

class EntityLyzardTest(unittest.TestCase):

    DOCS = [
            XMLContent(
            '''
            <?xml version="1.0" encoding="UTF-8"?>
            <wl:page xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:wl="http://www.weblyzard.com/wl/2013#" dc:title="" wl:id="99933" dc:format="text/html" xml:lang="de" wl:nilsimsa="030472f84612acc42c7206e07814e69888267530636221300baf8bc2da66b476" dc:related="http://www.heise.de http://www.kurier.at">
               <wl:sentence wl:id="50612085a00cf052d66db97ff2252544" wl:pos="NE NE VAFIN CARD NE NE VVPP $." wl:token="0,5 6,12 13,16 17,19 20,23 24,27 28,36 36,37" wl:sem_orient="0.0" wl:significance="0.0"><![CDATA[Georg Müller hat 10 Mio CHF gewonnen.]]></wl:sentence>
               <wl:sentence wl:id="a3b05957957e01060fd58af587427362" wl:pos="NN NE VMFIN APPR ART NN APPR CARD NE NE $, PRELS PPER NE NE VVFIN $, PIS VVINF $." wl:token="0,4 5,12 13,19 20,23 24,27 28,35 36,39 40,42 43,46 47,50 50,51 52,55 56,59 60,65 66,72 73,84 84,85 86,92 93,101 101,102" wl:sem_orient="0.0" wl:significance="0.0"><![CDATA[Herr Schmidt konnte mit dem Angebot von 10 Mio CHF, das ihm Georg Müller hinterlegte, nichts anfangen.]]></wl:sentence>
            </wl:page>
            ''').as_dict(),
            XMLContent(
            '''
            <?xml version="1.0" encoding="UTF-8"?>
            <wl:page xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:wl="http://www.weblyzard.com/wl/2013#" dc:title="" wl:id="99934" dc:format="text/html" xml:lang="de" wl:nilsimsa="020ee211a20084bb0d2208038548c02405bb0110d2183061db9400d74c15553a" dc:related="http://www.heise.de http://www.kurier.at">
               <wl:sentence wl:id="f98a0c4d2ddffd60b64b9b25f1f5657a" wl:pos="NN NE VVFIN $, KOUS ART NN ADV CARD ADJD VAINF VAFIN $." wl:token="0,6 7,14 15,23 23,24 25,29 30,33 34,37 38,42 43,47 48,59 60,64 65,69 69,70" wl:sem_orient="0.0" wl:significance="0.0"><![CDATA[Rektor Kessler erklärte, dass die HTW auch 2014 erfolgreich sein wird.]]></wl:sentence>
            </wl:page>
            ''').as_dict(),
               ]
     
    def test_entity_lyzard(self):
        docs = [ 
                 {'content_id': '12', 'content': u'Franz Klammer fährt Ski'}, 
                 {'content_id': '13', 'content' :u'Peter Müller macht Politik',} 
               ]

        e = Recognize()
        print e.list_profiles()
        e.add_profile('People.DACH.de')
        print e.search_documents('People.DACH.de', docs)

    def test_search_xml(self):
        e = Recognize()
        e.add_profile('People.DACH.de')
        print 'xmlsearch::::', e.search_documents('People.DACH.de', self.DOCS)

    def test_focus_search(self):
        e = Recognize()
        result =  e.get_focus(['People.DACH.de', 'extras.com.weblyzard.backend.recognize.extras.DataTypeProfile'], self.DOCS, max_results=3)

        # annotated two documents
        assert len(result) == len(self.DOCS)

        for content_id, res in result.items():
            print ':::', res
            assert u'focus' in res
            assert u'annotations' in res
    
    def test_geo(self):
        geodocs = [{'content_id': '11', 
                    'content': u'Frank goes to Los Angeles. Los Angeles is a nice city'},
               ]
        e = Recognize()
        profile_name = 'Cities.10000.en'
        
#        print e.list_configured_profiles()
#        print e.add_profile(profile_name, force=True)
#        
#        print 'list_configured_profiles', e.list_configured_profiles()
#        e.add_profile('Cities.10000.en')
#        
#        e.search_documents(profile_name=profile_name, 
#                           doc_list=geodocs, debug=True, 
#                           output_format='standard')
#        print 'list_profiles', e.list_profiles()
#        e.add_profile('Cities.10000.en', geodocs)
#        e.add_profile('Cities.10000.en')
        result = e.search('Cities.10000.en', geodocs, output_format='standard')
        print 'result', len(result), result[0]['name']
       
#    def test_geo_vs_geo(self):
#        docs = pickle.load(open('test_data_climate2_media.pickle'))
#        
#        for doc in docs['documents']:
#            print doc.get('geo_uri')
#            geocon = doc.get('content')
#            e = Recognize()
#            e.add_profile('Cities.10000.en', geocon)
#            #result = e.search('Cities.10000.en', geocon, max_entities=1, buckets=1, limit=1, output_format='standard')
#            print 'recognizeGeo:::', e.search('Cities.10000.en', geocon, max_entities=1, buckets=1, limit=1, output_format='standard')
   
    def test_password(self):
        test_cases = (
            ('http://test.net', 'test', 'password'),
            ('http://test.net', None, None), 
            (['http://test.net', 'http://test2.net'], 'test', 'password'), 
            (['http://test.net', 'http://test2.net'], None, None))
        
        for urls, user, password in test_cases: 
            correct_urls = Recognize.fix_urls(urls, user, password)
            assert isinstance(correct_urls, list)
            
            if isinstance(urls, basestring):
                assert len(correct_urls) == 1
            else: 
                assert len(urls) == len(correct_urls)
                
            for correct_url in correct_urls: 
                assert correct_url.endswith(Recognize.URL_PATH)
                user_password = '%s:%s@' % (user, password)
                if user and password: 
                    assert user_password in correct_url
                    ext_url, ext_user, ext_password = Retrieve.get_user_password(correct_url)
                    assert ext_user == user
                    assert ext_password == password
                    assert user_password not in ext_url
                else: 
                    assert user_password not in correct_url
                    
if __name__ == '__main__':
    unittest.main()

