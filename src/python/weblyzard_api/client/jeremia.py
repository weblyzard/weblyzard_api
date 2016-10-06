# -*- coding: utf-8 -*-

'''
.. codeauthor:: Albert Weichselbraun <albert.weichselbraun@htwchur.ch>
.. codeauthor:: Heinz-Peter Lang <lang@weblyzard.com>
'''
import logging
import urllib2

from time import sleep, time
from random import random

from eWRT.ws.rest import MultiRESTClient

from weblyzard_api.xml_content import XMLContent
from weblyzard_api.client import WEBLYZARD_API_URL, WEBLYZARD_API_USER, WEBLYZARD_API_PASS

logger = logging.getLogger('weblyzard_api.client.jeremia')

# number of seconds to wait if the web service is occupied
# - we stop once either DEFAULT_MAX_RETRY_DELAY or DEFAULT_MAX_RETRY_ATTEMPTS is reached
# . DEFAULT_WAIT_TIME should therefore amount to DEFAULT_MAX_RETRY_DELAY/2 * DEFAULT_MAX_RETRY_ATTEMPTS
DEFAULT_WAIT_TIME = 20 * 60
DEFAULT_MAX_RETRY_DELAY = 20
DEFAULT_MAX_RETRY_ATTEMPTS = 120

class Jeremia(MultiRESTClient):
    '''
    **Jeremia Web Service**

    Pre-processes text documents and returns an annotated webLyzard XML document.

    **Blacklisting**

    Blacklisting is an optional service which removes sentences which occur
    multiple times in different documents from these documents. Examples for such
    sentences are document headers or footers.

    The following functions handle sentence blacklisting:

     * :func:`clear_blacklist`
     * :func:`get_blacklist`
     * :func:`update_blacklist`

    Jeremia returns a
    :doc:`webLyzard XML document <weblyzard_api.data_format.xml_format>`.
    The weblyzard_api provides the class :class:`.XMLContent` to process
    and manipulate the weblyzard XML documents.:

    .. note:: Example usage

        .. code-block:: python

            from weblyzard_api.client.recognize import Recognize
            from pprint import pprint

            docs = {'id': '192292',
                    'title': 'The document title.',
                    'body': 'This is the document text...',
                    'format': 'text/html',
                    'header': {}}
            client = Jeremia()
            result = client.submit_document(docs)
            pprint(result)
    '''
    URL_PATH = 'jeremia/rest'
    ATTRIBUTE_MAPPING = {'content_id': 'id',
                         'title': 'title',
                         'sentences': 'sentence',
                         'lang': 'lang',
                         'sentences_map': {'pos': 'pos',
                                           'token': 'token',
                                           'value': 'value',
                                           'md5sum': 'id'}}

    def __init__(self, url=WEBLYZARD_API_URL, usr=WEBLYZARD_API_USER,
                 pwd=WEBLYZARD_API_PASS, default_timeout=None):
        '''
        :param url: URL of the jeremia web service
        :param usr: optional user name
        :param pwd: optional password
        '''
        MultiRESTClient.__init__(self, service_urls=url, user=usr, password=pwd,
                                 default_timeout=default_timeout)

    def submit_document(self, document):
        '''
        processes a single document with jeremia (annotates a single document)

        :param document: the document to be processed
        '''
        return self.request('submit_document', document)

    def submit_documents(self, documents, source_id=-1,
                         double_sentence_threshold=10,
                         wait_time=DEFAULT_WAIT_TIME,
                         max_retry_delay=DEFAULT_MAX_RETRY_DELAY,
                         max_retry_attempts=DEFAULT_MAX_RETRY_ATTEMPTS):
        '''
        :param batch_id: batch_id to use for the given submission
        :param documents: a list of dictionaries containing the document
        '''
        if not documents:
            raise ValueError('Cannot process an empty document list')

        request = 'submit_documents/%s/%d' % (source_id, double_sentence_threshold)

        # wait until the web service has available threads for processing
        # the request
        attempts = 0
        start_time = time()
        while time() - start_time < wait_time and attempts < max_retry_attempts:
            # wait until threads are available
            while self.has_queued_threads() and time() - start_time < wait_time:
                sleep(max_retry_delay * random())

            # submit the request
            # - here we need to check for a 502 and 503 error in
            #   case that has_queued_threads has not been
            #   up to date.
            try:
                result = self.request(request, documents,
                                      pass_through_exceptions=True)
                return result
            except (urllib2.HTTPError, urllib2.URLError) as e:
                attempts = attempts + 1

        # this access most certainly causes an exception since the
        # requests above have failed.
        return self.request(request, documents)


    def status(self):
        '''
        :returns: the status of the Jeremia web service.
        '''
        return self.request('status', return_plain=True)

    def version(self):
        '''
        :returns: the current version of the jeremia deployed on the server
        '''
        return self.request('version', return_plain=True)

    def get_xml_doc(self, text, content_id='1'):
        '''
        Processes text and returns a XMLContent object.

        :param text: the text to process
        :param content_id: optional content id
        '''
        batch = [{'id': content_id,
                  'title': '',
                  'body': text,
                  'format': 'text/plain'}]

        results = self.submit_documents(batch)
        result = results[0]
        return XMLContent(result['xml_content'])

    def update_blacklist(self, source_id, blacklist):
        '''
        updates an existing blacklist cache

        :param source_id: the blacklist's source id
        '''
        url = 'cache/update_blacklist/%s' % source_id
        return self.request(url, blacklist)

    def clear_blacklist(self, source_id):
        '''
        :param source_id: the blacklist's source id

        Empties the existing sentence blacklisting cache for the given source_id
        '''
        return self.request('cache/clear_blacklist/%s' % source_id)

    def get_blacklist(self, source_id):
        '''
        :param source_id: the blacklist's source id
        :returns: the sentence blacklist for the given source_id'''
        return self.request('cache/get_blacklist/%s' % source_id)

    def has_queued_threads(self):
        '''
        :returns:
            True if Jeremia still has queued (i.e. unprocessed) threads or
            False otherwise.

        :note:
            Submitting jobs if threads are queued is discouraged, since it
            will slow down the overall performance.
        '''
        try:
            result = self.request('has_queued_threads')
        except Exception as e:
            result = True
        return result
