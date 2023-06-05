#!/usr/bin/python
# -*- coding: utf8 -*-
"""
.. moduleauthor:: Albert Weichselbraun <albert.weichselbraun@htwchur.ch>
"""
from __future__ import unicode_literals

import urllib.error

from time import sleep, time
from random import random

from weblyzard_api.client import MultiRESTClient
from weblyzard_api.client import (WEBLYZARD_API_URL, WEBLYZARD_API_USER,
                                  WEBLYZARD_API_PASS)

import logging
logger = logging.getLogger(__name__)

# number of seconds to wait if the web service is occupied
# - we stop once either DEFAULT_MAX_RETRY_DELAY or DEFAULT_MAX_RETRY_ATTEMPTS is reached
# . DEFAULT_WAIT_TIME should therefore amount to DEFAULT_MAX_RETRY_DELAY/2 * DEFAULT_MAX_RETRY_ATTEMPTS
DEFAULT_WAIT_TIME = 20 * 60
DEFAULT_MAX_RETRY_DELAY = 20
DEFAULT_MAX_RETRY_ATTEMPTS = 120


class Recognize(MultiRESTClient):
    """
    Provides access to the RecognizeNg Web Service.

    **Workflow:**
     1. pre-load the recognize profiles you need using the :func:`load_profile` call.
     2. submit the text or documents to analyze using one of the following calls:

        * :func:`search_xmldocument` for jeremia documents.
        * :func:`search_text` for plain text.
        * :func:`search_document` for document dictionaries.
    """
    URL_PATH = 'rest/'
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
        """
        :param url: URL of the jeremia web service
        :param usr: optional user name
        :param pwd: optional password
        """
        MultiRESTClient.__init__(self, service_urls=url, user=usr, password=pwd,
                                 default_timeout=default_timeout)
        self.profile_cache = []

    def status(self):
        """
        :returns: the status of the Recognize web service.
        """
        return self.request(path='status')

    def load_profile(self, profile_name):
        """ Load a given profile.
        :param profile_name: name of the profile to load.
        """
        if profile_name in self.profile_cache:
            return

        self.profile_cache.append(profile_name)  # only try to add once
        return self.request(path='load_profile/{}'.format(profile_name))

    def list_profiles(self):
        """ List all loaded profiles.
        :returns: a list of all pre-loaded profiles
            .. code-block:: python
            >>> r=Recognize()
            >>> r.list_profiles()
            [u"MAXIMUM.COVERAGE",u"JOBCOCKPIT"]
        """
        return self.request('list_profiles')

    def get_searcher_content(self, profile_name, entity_url):
        """
        Returns searcher content for entity url and profile.
        :param profile_name: the profile to search in
        :param entity_url: long entity URL.
        """
        content_type = 'application/json; charset=utf-8'

        return self.request(path='getSearcherContent',
                            content_type=content_type,
                            query_parameters={'profileName': profile_name,
                                              'entityKey': entity_url})

    def search_text(self, profile_name, lang, text):
        """
        Search text for entities specified in the given profiles.
        :param profile_name: the profile to search in
        :param text: the text to search in
        :param limit: maximum number of results to return
        :rtype: the tagged text
        """
        content_type = 'application/json'

        return self.request(path='corpus/annotate_unknown',
                            parameters=text,
                            content_type=content_type,
                            query_parameters={'profileName': profile_name,
                                              'lang': lang})

    def search_document(self, profile_name, document, limit=0):
        """
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
        """
        if not document:
            return

        content_type = 'application/json; charset=utf-8'
        search_command = 'search_document'
        return self.request(path=search_command,
                            parameters=document,
                            content_type=content_type,
                            query_parameters={'profileName': profile_name,
                                              'limit': limit
                                              })

    def search_xmldocument(self, profile_name, document, limit):
        """
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
        """
        if not document:
            return

        content_type = 'application/json'
        return self.request(path='search_xmldocument',
                            parameters=document,
                            content_type=content_type,
                            query_parameters={'profileName': profile_name,
                                              'limit': limit
                                              })

    def search_documents(self, profile_name, document_list, limit,
                         wait_time=DEFAULT_WAIT_TIME,
                         max_retry_delay=DEFAULT_MAX_RETRY_DELAY,
                         max_retry_attempts=DEFAULT_MAX_RETRY_ATTEMPTS):
        """
        Search the given document for entities specified in the given profiles.
        :param profile_name: the profile to search in
        :param document_list: a list of documents to search in
        :param limit: maximum number of results to return
        :rtype: the tagged text
        """
        if not document_list:
            return

        content_type = 'application/json'
        search_command = 'search_documents'

        # wait until the web service has available threads for processing
        # the request
        attempts = 0
        start_time = time()
        while time() - start_time < wait_time and attempts < max_retry_attempts:

            # submit the request
            # - here we need to check for a 502 and 503 error in
            #   case that has_queued_threads has not been
            #   up to date.
            try:
                result = self.request(path=search_command,
                            parameters=document_list,
                            content_type=content_type,
                            query_parameters={'profileName': profile_name,
                                              'limit': limit
                                              })
                return result
            except (urllib.error.HTTPError, urllib.error.URLError) as e:
                sleep(max_retry_delay * random())
                attempts = attempts + 1

        return self.request(path=search_command,
                            parameters=document_list,
                            content_type=content_type,
                            query_parameters={'profileName': profile_name,
                                              'limit': limit
                                              })
