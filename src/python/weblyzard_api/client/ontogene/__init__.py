#!/usr/bin/python
# -*- coding: utf8 -*-
'''
.. moduleauthor:: Adrian Brasoveanu <adrian.brasoveanu@htwchur.ch>
.. moduleauthor:: Albert Weichselbraun <albert.weichselbraun@fhgr.ch>
'''
import logging
import requests
import json

from weblyzard_api.client import OGER_API_URL

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT_SEC = 45
DEFAULT_MAX_RETRY_DELAY = 15
DEFAULT_MAX_RETRY_ATTEMPTS = 5


class OgerClient(object):
    '''
    Provides access to the OntoGene Entity Recognition.

    The client sends a weblyzardDocument to the OGER web services,
    and retrieves an annotated version of the document.
    '''
    # available endpoints
    ANNOTATE_PATH = 'upload'  # /txt/bioc_json
    STATUS_PATH = 'status'

    def __init__(self, url=OGER_API_URL,
                 service_timeout=DEFAULT_TIMEOUT_SEC):
        '''
        :param url: URL of the OGER web service
        :param timeout: optional timeout for service responses
        '''
        if isinstance(url, list):
            raise Exception('Oger url cannot be an array')
        if url.endswith('/'):
            url = url[:-1]
        self.url = url
        self.service_timeout = service_timeout

    def status(self):
        '''
        :returns: the status of the OGER web service.
        '''
        url = '/'.join([self.url, self.STATUS_PATH])
        return requests.get(url, timeout=self.service_timeout).json()

    @staticmethod
    def generate_weblyzard_document(docid, doctext):
        '''
        Generates the weblyzard document based on the input text and id.

        :param docid: the document's ID.
        :param doctext: the document's content to be annotated.
        :returns: the weblyzard documet.
         '''
        return {
           "id": docid,
           "header": {"{http://purl.org/dc/elements/1.1/}identifier": docid,
                      "{http://www.weblyzard.com/wl/2013#}jonas_type": "http"},
           "partitions": {},
           "annotations": [],
           "content": doctext
        }

    def annotate_text(self, docid, doctext):
        '''
        Annotate a document's text content with the OGER annotation service.

        :param docid: the document's ID.
        :param doctext: the document's content to be annotated.
        :returns: OGER annotated document after uploading a text.
        '''
        weblyzard_document = OgerClient.generate_weblyzard_document(docid,
                                                                    doctext)
        return self.annotate_weblyzard_document(weblyzard_document)

    def annotate_weblyzard_document(self, weblyzard_document):
        '''
        Annotate a document's text content with the OGER annotation service.
        :param weblyzard_document: the weblyzard document to annotate
        :returns: the annotated weblyzard document or the original document
            in case something went wrong.
        '''
        url = '/'.join([self.url, self.ANNOTATE_PATH])
        r = requests.post(url=url, data=json.dumps(weblyzard_document),
                          timeout=self.service_timeout)
        if r.status_code == 200:
            return json.loads(r.content)
        else:
            logging.warn("OGER server returned status code "
                         +str(r.status_code) + " and message "
                         +str(r.content))
            logging.warn("Falling back to the unannotated content.")
            return weblyzard_document
