#!/usr/bin/python
# -*- coding: utf8 -*-
'''
.. moduleauthor:: Albert Weichselbraun <albert.weichselbraun@htwchur.ch> 
'''
import logging

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
