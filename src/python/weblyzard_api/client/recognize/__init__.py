#!/usr/bin/python
# -*- coding: utf8 -*-
'''
.. moduleauthor:: Albert Weichselbraun <albert.weichselbraun@htwchur.ch> 
'''
import logging
import unittest
from pprint import pprint

from eWRT.access.http import Retrieve
from eWRT.ws.rest import MultiRESTClient

from weblyzard_api.xml_content import XMLContent
from weblyzard_api.client import (WEBLYZARD_API_URL, WEBLYZARD_API_USER,
                                  WEBLYZARD_API_PASS)

INTERNAL_PROFILE_PREFIX = 'extras.'
LOGGER = logging.getLogger('weblyzard_api.client.recognize')
SUPPORTED_LANGS = ('en', 'fr', 'de')

class Recognize(MultiRESTClient):
    '''
    Provides access to the Recognize Web Service.
    
    **Workflow:**
     1. pre-load the recognize profiles you need using the :func:`add_profile` call.
     2. submit the text or documents to analyze using one of the following calls:
         
        * :func:`search_document` or :func:`search_documents` for document dictionaries.
        * :func:`search_text` for plain text.
    
    .. note:: Example usage
    
        .. code-block:: python
    
            from weblyzard_api.client.recognize import Recognize
            from pprint import pprint
            
            url = 'http://triple-store.ai.wu.ac.at/recognize/rest/recognize'
            profile_names = ['en.organization.ng', 'en.people.ng', 'en.geo.500000.ng']
            text = 'Microsoft is an American multinational corporation 
                    headquartered in Redmond, Washington, that develops, 
                    manufactures, licenses, supports and sells computer 
                    software, consumer electronics and personal computers 
                    and services. It was was founded by Bill Gates and Paul
                    Allen on April 4, 1975.'
            
            client = Recognize(url)
            result = client.search_text(profile_names,
                        text,
                        output_format='compact',
                        max_entities=40,
                        buckets=40,
                        limit=40)  
            pprint(result)
    '''
    OUTPUT_FORMATS = ('standard', 'minimal', 'annie', 'compact')
    URL_PATH = 'recognize/rest/recognize'
    ATTRIBUTE_MAPPING = {'content_id': 'id',
                         'lang': 'xml:lang',
                         'sentences' : 'sentence',
                         'sentences_map': {'pos': 'pos',
                                           'token': 'token',
                                           'md5sum': 'id',
                                           'value': 'value'}}

    def __init__(self, url=WEBLYZARD_API_URL, usr=WEBLYZARD_API_USER, 
                 pwd=WEBLYZARD_API_PASS, default_timeout=None):
        '''
        :param url: URL of the jeremia web service
        :param usr: optional user name
        :param pwd: optional password
        '''
        MultiRESTClient.__init__(self, service_urls=url, user=usr, password=pwd, 
                                 default_timeout=default_timeout)
        self.profile_cache = []

    @classmethod
    def convert_document(cls, xml):
        ''' converts an XML String to a document dictionary necessary for \
            transmitting the document to Recognize.

        :param xml: weblyzard_xml representation of the document
        :returns: the converted document
        :rtype: dict

        .. note::
            non-sentences are ignored and titles are added based on the
            XmlContent's interpretation of the document.
        '''
        if not isinstance(xml, XMLContent):
            xml = XMLContent(xml)

        return xml.as_dict(mapping=cls.ATTRIBUTE_MAPPING,
                           ignore_non_sentence=False,
                           add_titles_to_sentences=True)

    def list_profiles(self):
        ''' :returns: a list of all pre-loaded profiles

            .. code-block:: python

            >>> r=Recognize()
            >>> r.list_profiles()
            [u'Cities.DACH.10000.de_en', u'People.DACH.de']
        '''
        return self.request('list_profiles')

    def list_configured_profiles(self):
        ''' :returns: a list of all profiles supported in the current \
                configuration '''
        return self.request('list_configured_profiles')

    def add_profile(self, profile_name, force=False):
        ''' pre-loads the given profile 

        ::param profile_name: name of the profile to load.
        '''
        if profile_name.startswith(INTERNAL_PROFILE_PREFIX):
            return
        
        profile_exists = profile_name in self.profile_cache and not force
        if not profile_exists:
            profile_exists = profile_name in self.list_profiles() and not force

        if profile_exists and not profile_name in self.profile_cache:
            self.profile_cache.append(profile_name)

        if not profile_exists:
            self.profile_cache.append(profile_name) #only try to add once
            return self.request('add_profile/%s' % profile_name)

    def get_xml_document(self, document):
        ''' :returns: the correct XML representation required by the Recognize \
            service'''
        return document.xml_content.as_dict(self.ATTRIBUTE_MAPPING)

    def remove_profile(self, profile_name):
        ''' removes a profile from the list of pre-loaded profiles '''
        return self.request('remove_profile/%s' % profile_name)

    def search_text(self, profile_names, text, debug=False, max_entities=1,
            buckets=1, limit=1, output_format='minimal'):
        '''
        Search text for entities specified in the given profiles.

        :param profile_names: the profile to search in
        :param text: the text to search in
        :param debug: compute and return an explanation
        :param buckets: only return n buckets of hits with the same score
        :param max_entities: number of results to return (removes the top \
            hit's tokens and rescores the result list subsequently
        :param limit: only return that many results
        :param output_format: the output format to use ('standard', \
            *'minimal'*, 'annie')
        :rtype: the tagged text
        '''
        assert output_format in self.OUTPUT_FORMATS
        if isinstance(profile_names, basestring):
            profile_names = (profile_names, )

        for profile_name in profile_names:
            self.add_profile(profile_name)

        return self.request(path='search',
                            parameters=text,
                            query_parameters={'profileNames' : profile_names,
                                              'rescore': max_entities,
                                              'buckets': buckets,
                                              'limit': limit,
                                              'wt': output_format,
                                              'debug': debug})


    def search_document(self, profile_names, document, debug=False,
                         max_entities=1, buckets=1, limit=1,
                         output_format='minimal'):
        '''
        :param profile_names: a list of profile names
        :param document: a single document to analyze (see example documents \
            below)
        :param debug: compute and return an explanation
        :param buckets: only return n buckets of hits with the same score
        :param max_entities: number of results to return (removes the top hit's \
            tokens and rescores the result list subsequently
        :param limit: only return that many results
        :param output_format: the output format to use ('standard', *'minimal'*, \
            'annie')
        :rtype: the tagged dictionary

        .. note:: Example document

           .. code-block:: python
   
              # option 1: document dictionary
              {'content_id': 12, 
               'content': u'the text to analyze'}

              # option 2: weblyzardXML
              XMLContent('<?xml version="1.0"...').as_list()

        .. note:: Corresponding web call

            http://localhost:8080/recognize/searchXml/ofwi.people
        '''
        assert output_format in self.OUTPUT_FORMATS
        if not document:
            return
        if isinstance(profile_names, basestring):
            profile_names = [profile_names, ]


        for profile_name in profile_names:
            try:
                self.add_profile(profile_name)
            except Exception:
                profile_names.remove(profile_name)
                msg = 'could not load profile %s, skipping' % profile_name
                LOGGER.warn(msg)

        content_type = 'application/json'

        if 'content_id' in document:
            search_command = 'search'
        elif 'id' in document:
            search_command = 'searchXml'
        else:
            raise ValueError("Unsupported input format.")

        return self.request(path=search_command,
                            parameters=document,
                            content_type=content_type,
                            query_parameters={'profileNames' : profile_names,
                                              'rescore': max_entities,
                                              'buckets': buckets,
                                              'limit': limit,
                                              'wt': output_format,
                                              'debug': debug})

    def search_documents(self, profile_names, doc_list, debug=False,
                         max_entities=1, buckets=1, limit=1,
                         output_format='compact'):
        '''
        :param profile_names: a list of profile names
        :param doc_list: a list of documents to analyze (see example below)         
        :param debug: compute and return an explanation
        :param buckets: only return n buckets of hits with the same score
        :param max_entities: number of results to return (removes the top \
            hit's tokens and rescores the result list subsequently
        :param limit: only return that many results
        :param output_format: the output format to use ('standard', \
            *'minimal'*, 'annie')
        :rtype: the tagged dictionary

        .. note:: Example document

           .. code-block:: python
   
              # option 1: list of document dictionaries
              ( {'content_id': 12,
                 'content': u'the text to analyze'})

              # option 2: list of weblyzardXML dictionary representations
              (XMLContent('<?xml version="1.0"...').as_list(),
               XMLContent('<?xml version="1.0"...').as_list(),)
         '''
        assert output_format in self.OUTPUT_FORMATS
        if not doc_list or len(doc_list) == 0:
            return
        if isinstance(profile_names, basestring):
            profile_names = (profile_names, )


        profiles_to_add = []
        for profile_name in profile_names:
            for lang in SUPPORTED_LANGS:
                if profile_name.startswith(lang):
                    profiles_to_add.append(profile_name)

        remaining = set(profile_names).difference(set(profiles_to_add))
        if len(remaining):
            #get all required languages from documents
            lang_list = []
            for document in doc_list:
                if 'lang' in document:
                    lang_list.append(document['lang'])
            lang_list = set(lang_list)

            #add required profiles
            if isinstance(profile_names, dict):
                for lang in lang_list:
                    if lang in profile_names:
                        for profile_name in profile_names[lang]:
                            profiles_to_add.append(profile_name)
            else:
                for profile_name in profile_names:
                    profiles_to_add.append(profile_name)

        #add required profiles
        for profile_name in set(profiles_to_add):
            self.add_profile(profile_name)

        content_type = 'application/json'

        if 'content_id' in doc_list[0]:
            search_command = 'searchDocuments'
        elif 'id' in doc_list[0]:
            search_command = 'searchXmlDocuments'
        else:
            raise ValueError("Unsupported input format.")

        return self.request(path=search_command,
                            parameters=doc_list,
                            content_type=content_type,
                            query_parameters={
                                              'profileNames' : profile_names,
                                              'rescore': max_entities,
                                              'buckets': buckets,
                                              'limit': limit,
                                              'wt': output_format,
                                              'debug': debug})

    def get_focus(self, profile_names, doc_list, max_results=1):
        '''
        :param profile_names: a list of profile names
        :param doc_list: a list of documents to analyze based on the \
                         weblyzardXML format
        :param max_results: maximum number of results to include
        :returns: the focus and annotation of the given document

        .. note:: Corresponding web call

           http://localhost:8080/recognize/focus?profiles=ofwi.people&profiles=ofwi.organizations.context
        '''
        if isinstance(profile_names, basestring):
            profile_names = (profile_names, )

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
        '''
        :returns: the status of the Recognize web service.
        '''
        return self.request(path='status')


class TestRecognize(unittest.TestCase):
 
    DOCS_XML = [
            '''
            <?xml version="1.0" encoding="UTF-8"?>
            <wl:page xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:wl="http://www.weblyzard.com/wl/2013#" dc:title="" wl:id="99933" dc:format="text/html" xml:lang="de" wl:nilsimsa="030472f84612acc42c7206e07814e69888267530636221300baf8bc2da66b476" dc:related="http://www.heise.de http://www.kurier.at">
               <wl:sentence wl:id="50612085a00cf052d66db97ff2252544" wl:pos="NE NE VAFIN CARD NE NE VVPP $." wl:token="0,5 6,12 13,16 17,19 20,23 24,27 28,36 36,37" wl:sem_orient="0.0" wl:significance="0.0"><![CDATA[Georg Müller hat 10 Mio CHF gewonnen.]]></wl:sentence>
               <wl:sentence wl:id="a3b05957957e01060fd58af587427362" wl:pos="NN NE VMFIN APPR ART NN APPR CARD NE NE $, PRELS PPER NE NE VVFIN $, PIS VVINF $." wl:token="0,4 5,12 13,19 20,23 24,27 28,35 36,39 40,42 43,46 47,50 50,51 52,55 56,59 60,65 66,72 73,84 84,85 86,92 93,101 101,102" wl:sem_orient="0.0" wl:significance="0.0"><![CDATA[Herr Schmidt konnte mit dem Angebot von 10 Mio CHF, das ihm Georg Müller hinterlegte, nichts anfangen.]]></wl:sentence>
            </wl:page>
            ''',
            '''
            <?xml version="1.0" encoding="UTF-8"?>
            <wl:page xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:wl="http://www.weblyzard.com/wl/2013#" dc:title="" wl:id="99934" dc:format="text/html" xml:lang="de" wl:nilsimsa="020ee211a20084bb0d2208038548c02405bb0110d2183061db9400d74c15553a" dc:related="http://www.heise.de http://www.kurier.at">
               <wl:sentence wl:id="f98a0c4d2ddffd60b64b9b25f1f5657a" wl:pos="NN NE VVFIN $, KOUS ART NN ADV CARD ADJD VAINF VAFIN $." wl:token="0,6 7,14 15,23 23,24 25,29 30,33 34,37 38,42 43,47 48,59 60,64 65,69 69,70" wl:sem_orient="0.0" wl:significance="0.0"><![CDATA[Rektor Kessler erklärte, dass die HTW auch 2014 erfolgreich sein wird.]]></wl:sentence>
            </wl:page>
            ''']
 
    
    #we need to get the recognize client twice (once here and once in setUp)
 
    TESTED_PROFILES = ['de.people.ng', 'en.geo.500000.ng', 'en.organization.ng', 'en.people.ng']
    IS_ONLINE = True
     
    def setUp(self):
        self.available_profiles = []
        url = 'http://voyager.srv.weblyzard.net:8080/recognize/rest/recognize'
        self.client = Recognize(url)
        self.service_is_online = self.client.is_online()
        if not self.service_is_online:
            print 'WARNING: Webservice is offline --> not executing all tests!!'
            self.IS_ONLINE = False
            return
             
        recognize_profiles = self.client.list_profiles()
        for profile in recognize_profiles:
            if profile in self.TESTED_PROFILES:
                self.available_profiles.append(profile)
  
        self.all_profiles = self.client.list_profiles()
        self.DOCS = [Recognize.convert_document(xml) for xml in self.DOCS_XML]
        
#     def test_adrian(self):
# 
#         from pprint import pprint
#         
# 
#         print "start"
#     
#         #url = 'http://triple-store.ai.wu.ac.at:8080/recognize/rest/recognize'
#         url = 'http://voyager.srv.weblyzard.net:8080/recognize/rest/recognize'
#         client = Recognize(url)
#         profile_names=['en.organization.ng', 'en.people.ng', 'en.geo.500000.ng']
#         text = 'Microsoft is an American multinational corporation headquartered in Redmond, Washington, that develops, manufactures, licenses, supports and sells computer software, consumer electronics and personal computers and services. It was was founded by Bill Gates and Paul Allen on April 4, 1975.'
#     
#         client.add_profile('en.organization.ng')
#         
#         result = client.search_text(profile_names,
#                                     text,
#                                     output_format='compact',
#                                     max_entities=40,
#                                     buckets=40,
#                                     limit=40)
#         pprint(result)
#         print "end"
            
    def test_missing_profiles(self):
        self.missing_profiles = []
  
        if self.IS_ONLINE and self.service_is_online:
            if len(self.available_profiles) == len(self.TESTED_PROFILES):
                print "All profiles are available on the current server"
            else:
                for profile in self.TESTED_PROFILES:
                    if profile not in self.available_profiles:
                        self.missing_profiles.append(profile)
                print "Missing profiles: ", self.missing_profiles
   
    def test_entity_lyzard(self):
        docs = [{'content_id': '12', 'content': u'Franz Klammer fährt Ski'},
                {'content_id': '13', 'content' :u'Peter Müller macht Politik'}]
   
        required_profile = 'de.people.ng'
        if required_profile not in self.available_profiles:
            print "Profile %s not available!" % required_profile
            return
        #we test if we can add profiles and if a German profile works
        if self.IS_ONLINE and self.service_is_online:
            print self.client.list_profiles()
            self.client.add_profile('de.people.ng')
            print self.client.search_documents('de.people.ng', docs)
             
    def test_search_xml(self):
        required_profile = 'de.people.ng'
        if required_profile not in self.available_profiles:
            print "Profile %s not available!" % required_profile
            return
          
        if self.IS_ONLINE and self.service_is_online:
            self.client.add_profile('de.people.ng')
            result = self.client.search_documents('de.people.ng', self.DOCS)
            print 'xmlsearch::::', result
 
    def test_focus_search(self):
        required_profile = 'de.people.ng'
        if required_profile not in self.available_profiles:
            print "Profile %s not available!" % required_profile
            return
          
        if self.IS_ONLINE and self.service_is_online:
            pn = 'extras.com.weblyzard.backend.recognize.extras.DataTypeProfile'
            result = self.client.get_focus(['de.people.ng', pn],
                                           self.DOCS, max_results=3)
   
            # annotated two documents
            assert len(result) == len(self.DOCS)
   
            for res in result.itervalues():
                print ':::', res
                assert u'focus' in res
                assert u'annotations' in res
  
    def test_geo(self):
        required_profile = 'en.geo.500000.ng'
        if required_profile not in self.available_profiles:
            print "Profile %s not available!" % required_profile
            return
 
        geodocs = [{'content_id': '11',
                    'content': u'Frank goes to Los Angeles. Los Angeles is a nice city'},
               ]
  
        if self.IS_ONLINE and self.service_is_online:
            profile_name = 'en.geo.500000.ng'
      
            print self.client.list_configured_profiles()
            print self.client.add_profile(profile_name, force=True)
     
            print 'list_configured_profiles', self.client.list_configured_profiles()
            self.client.add_profile('Cities.10000.en')
     
            self.client.search_documents(profile_name=profile_name,
                               doc_list=geodocs, debug=True,
                               output_format='standard')
            print 'list_profiles', self.client.list_profiles()
            self.client.add_profile('Cities.10000.en', geodocs)
            self.client.add_profile('Cities.10000.en')
            result = self.client.search_documents(profile_name, geodocs, output_format='compact')
            first = result['11']
            print 'result', len(result), first[0]['preferredName']
 
    def test_geo_swiss(self):
        '''
        Tests the geo annotation service for Swiss media samples.
         
        .. note::
 
            ``de_CH.geo.5000.ng`` detects Swiss cities with more than 5000
            and worldwide cities with more than 500,000 inhabitants.
        '''
        required_profile = 'de_CH.geo.5000.ng'
        if required_profile not in self.available_profiles:
            print("Profile %s not available!" % required_profile)
            return
 
        if 'noah.semanticlab.net' not in self.client.url:
            print("This test is only run on noah...\n...skipping test.")
  
        self.client.add_profile(required_profile)
 
   
    def test_organization(self):
        required_profile = 'en.organization.ng'
        if required_profile not in self.available_profiles:
            print "Profile %s not available!" % required_profile
            return
                  
        docs = [{'content_id': '14', 'content': u'Bill Gates was the CEO of Microsoft.'},
                {'content_id': '15', 'content' :u'Facebook is largest social networks.'}]
   
        if self.IS_ONLINE and self.service_is_online:
            print self.client.list_profiles()
            self.client.add_profile('en.organization.ng')
            print self.client.search_documents('en.organization.ng', docs)
   
    def test_people(self):
        required_profile = 'en.people.ng'
        if required_profile not in self.available_profiles:
            print "Profile %s not available!" % required_profile
            return
          
        docs = [{'content_id': '16', 'content': u'George W. Bush is a former President.'},
                {'content_id': '17', 'content' :u'Mark Zuckerberg speaks Chinese.'}]
   
        if self.IS_ONLINE and self.service_is_online:
            print self.client.list_profiles()
            self.client.add_profile('en.people.ng')
            print self.client.search_documents('en.people.ng', docs)
   
   
    def test_date_profile(self):
        """ """
        docs = [{'content_id': '12', 'content': u'Franz Klammer fährt gestern Ski, 12th September 2014 are we feeling better'}]
        #                 {'content_id': '13', 'content' :u'Peter Müller macht Politik'}]
        profile = 'extras.com.weblyzard.backend.recognize.extras.DateTimeProfile'
        #         assert self.IS_ONLINE and self.service_is_online
        #         assert profile in self.available_profiles
         
        result = self.client.search_documents(profile_names=[profile], doc_list=docs)
        print result
           
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
  
    def test_swiss_profile(self):
        required_profile = 'de_CH.geo.5000.ng'
        client = Recognize()
        # client.remove_profile(required_profile)
        client.add_profile(required_profile)
        for text in 'Haldenstein liegt in der Nähe von Landquart.', 'Sargans hat einen wichtigen Bahnhof', 'Vinzenz arbeitet in Winterthur':
            result = client.search_text(required_profile, text, output_format='compact' )
            print(result)
      
        required_profile = 'snf.media.criticism.project'
        client.add_profile(required_profile)
        print client.search_text(required_profile, "Die SRG und die SRF sind sehr kritisch was das Engagement der NZZ betrifft", output_format='compact')
        print client.search_text(required_profile, "die srg und die srf sind sehr kritisch was das engagement der nzz betrifft", output_format='compact')

if __name__ == '__main__':
    unittest.main()



