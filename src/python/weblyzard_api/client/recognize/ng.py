#!/usr/bin/python
# -*- coding: utf8 -*-
'''
.. moduleauthor:: Albert Weichselbraun <albert.weichselbraun@htwchur.ch>
'''
import logging

from eWRT.ws.rest import MultiRESTClient

from weblyzard_api.client import (WEBLYZARD_API_URL, WEBLYZARD_API_USER,
                                  WEBLYZARD_API_PASS)
from weblyzard_api.xml_content import XMLContent

INTERNAL_PROFILE_PREFIX = 'extras.'
LOGGER = logging.getLogger('weblyzard_api.client.recognize.ng')
SUPPORTED_LANGS = ('en', 'fr', 'de')


class Recognize(MultiRESTClient):
    '''
    Provides access to the RecognizeNg Web Service.

    **Workflow:**
     1. pre-load the recognize profiles you need using the :func:`load_profile` call.
     2. submit the text or documents to analyze using one of the following calls:

        * :func:`search_xmldocument` for jeremia documents.
        * :func:`search_text` for plain text.
        * :func:`search_document` for document dictionaries.
    '''
    OUTPUT_FORMATS = ('standard', 'minimal', 'annie', 'compact')
    URL_PATH = '/recognize/rest/'
    ATTRIBUTE_MAPPING = {'content_id': 'id',
                         'lang': 'lang',
                         'format': 'format',
                         'nilsimsa': 'nilsimsa',
                         'sentences': 'sentences',
                         'sentences_map': {'pos': 'pos',
                                           'token': 'token',
                                           'significance': 'significance',
                                           'is_title': 'is_title',
                                           'md5sum': 'md5sum',
                                           'value': 'text',
                                           'dependency': 'dependency'}}

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
    def convert_document(cls, xml, version='0.4'):
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

        try:
            if float(version[0:3]) >= 0.5:
                return xml.get_xml_document(xml_version=2013).strip()
        except Exception as e:
            LOGGER.warn('Could not parse version: %s' % version)
        return xml.as_dict(mapping=cls.ATTRIBUTE_MAPPING,
                           ignore_features=True,
                           ignore_relations=True,
                           ignore_non_sentence=False,
                           add_titles_to_sentences=True)

    def get_xml_document(self, document):
        ''' :returns: the correct XML representation required by the Recognize \
            service'''
        print(document)
        return document.xml_content.as_dict(self.ATTRIBUTE_MAPPING)

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

        self.profile_cache.append(profile_name)  # only try to add once
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
                            query_parameters={'profileName': profile_name,
                                              'lang': lang})

    def search_document(self, profile_name, document, limit=0):
        '''
        :param profile_name: profile name
        :param document: a single document to analyze (see example documents \
            below)
        :param limit: only return that many results

        .. note:: Example document

           .. code-block:: python

              # option 1: document dictionary
              {'content_id': 12, 
               'content': u'the text to analyze'}

              # option 2: weblyzardXML
              XMLContent('<?xml version="1.0"...').as_list()
        '''
        if not document:
            return

        content_type = 'application/json'
        search_command = 'search_document'
        return self.request(path=search_command,
                            parameters=document,
                            content_type=content_type,
                            query_parameters={'profileName': profile_name,
                                              'limit': limit
                                              })

    def search_xmldocument(self, profile_name, document, limit):
        '''
        Search the given document for entities specified in the given profiles.
        This should only be called with Jeremia results.

        .. note:: Example document

           .. code-block:: python     
                test_doc = {'id': 111,
                            'body': 'Management Directive\nBill Gates\n Java Programmer',
                            'title': 'Hello President! ',
                            'format': 'text/html',
                            'header': {}}

                jeremia_client = Jeremia()
                jresult = jeremia_client.submit_document(test_doc2)
                newresult = r.search_xmldocument(profile_name=profile, document=jresult, limit=0)   


        :param profile_name: the profile to search in
        :param document: the document to search in
        :param limit: maximum number of results to return
        '''
        #assert output_format in self.OUTPUT_FORMATS
        if not document:
            return

        content_type = 'application/json'
        return self.request(path='search_xmldocument',
                            parameters=document,
                            content_type=content_type,
                            query_parameters={'profileName': profile_name,
                                              'limit': limit
                                              })

    def search_documents(self, profile_name, document_list, limit):
        '''
        Search the given document for entities specified in the given profiles.

        :param profile_name: the profile to search in
        :param document_list: a list of documents to search in
        :param limit: maximum number of results to return
        :rtype: the tagged text
        '''
        raise NotImplementedError
