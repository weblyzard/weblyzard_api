#!/usr/bin/python
# -*- coding: utf8 -*-
'''
.. moduleauthor:: Albert Weichselbraun <albert.weichselbraun@htwchur.ch>
'''
import logging

from eWRT.ws.rest import MultiRESTClient
from weblyzard_api.client import (WEBLYZARD_API_URL, WEBLYZARD_API_USER,
                                  WEBLYZARD_API_PASS)

INTERNAL_PROFILE_PREFIX = 'extras.'
LOGGER = logging.getLogger('weblyzard_api.client.recognize.ng')
SUPPORTED_LANGS = ('en', 'fr', 'de')

class Recognize(MultiRESTClient):
    '''
    Provides access to the Recognize Web Service.

    **Workflow:**
     1. pre-load the recognize profiles you need using the :func:`load_profile` call.
     2. submit the text or documents to analyze using one of the following calls:

        * :func:`search_document` or :func:`search_documents` for document dictionaries.
        * :func:`search_text` for plain text.

    .. note:: Example usage

        .. code-block:: python

            from weblyzard_api.client.recognize import Recognize
            from pprint import pprint

            url = 'http://triple-store.ai.wu.ac.at/recognize/rest/recognize'
            profile_name = 'en_US'
            text = 'Microsoft is an American multinational corporation
                    headquartered in Redmond, Washington, that develops,
                    manufactures, licenses, supports and sells computer
                    software, consumer electronics and personal computers
                    and services. It was was founded by Bill Gates and Paul
                    Allen on April 4, 1975.'

            client = Recognize(url)
            result = client.search_text(profile_name,
                        text,
                        limit=40)
            pprint(result)
    '''
    URL_PATH = '/recognize/rest/'
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

    def status(self):
        '''
        :returns: the status of the Recognize web service.
        '''
        return self.request(path='status')
    
    def load_profile(self, profile_name):
        ''' pre-loads the given profile

        ::param profile_name: name of the profile to load.
        '''
        if profile_name.startswith(INTERNAL_PROFILE_PREFIX) or profile_name in self.profile_cache:
            return

        self.profile_cache.append(profile_name)                 #only try to add once
        return self.request(path='load_profile/{}'.format(profile_name))
    
    def list_profiles(self):
        ''' :returns: a list of all pre-loaded profiles
            .. code-block:: python
            >>> r=Recognize()
            >>> r.list_profiles()
            [u"MAXIMUM.COVERAGE",u"JOBCOCKPIT"]
        '''
        return self.request('list_profiles')

    def search_text(self, profile_name, lang, text):
        '''
        Search text for entities specified in the given profiles.

        :param profile_name: the profile to search in
        :param text: the text to search in
        :param limit: maximum number of results to return
        :rtype: the tagged text
        '''
        content_type = 'application/json'

        return self.request(path='search_text',
                            parameters=text,
                            content_type=content_type,
                            query_parameters={'profileName' : profile_name,
                                              'lang': lang})


    def search_document(self, profile_name, document):
        '''
        Search the given document for entities specified in the given profiles.

        :param profile_name: the profile to search in
        :param document: the document to search in
        :param limit: maximum number of results to return
        :rtype: the tagged text
        '''
        #assert output_format in self.OUTPUT_FORMATS
        if not document:
            return

        content_type = 'application/json; charset=utf-8'
        
        if 'content_id' in document:
            search_command = 'search_xmldocument'
        elif 'id' in document:
            search_command = 'search_xmldocument'
        else:
            raise ValueError("Unsupported input format.")
        
        print(search_command)
        
        return self.request(path='search_xmldocument',
                            parameters=document,
                            content_type=content_type,
                            query_parameters={'profileName' : profile_name
                                              #'rescore': max_entities,
                                              #'buckets': buckets,
                                              #'wt': output_format,
                                              #'debug': debug
                                              })
    
    '''
            Response response =
                super.getTarget(SEARCH_DOCUMENT_SERVICE_URL)
                        .queryParam(PARAM_PROFILE_NAME, profileName)
                        .queryParam(PARAM_LIMIT, limit)
                        .request(MediaType.APPLICATION_JSON_TYPE)
                        .post(Entity.json(data));
    '''

    def search_documents(self, profile_name, document_list, limit):
        '''
        Search the given document for entities specified in the given profiles.

        :param profile_name: the profile to search in
        :param document_list: a list of documents to search in
        :param limit: maximum number of results to return
        :rtype: the tagged text
        '''
        raise NotImplementedError

