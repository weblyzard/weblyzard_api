#!/usr/bin/python
# -*- coding: utf8 -*-
"""
.. moduleauthor:: Adrian Brasoveanu <adrian.brasoveanu@htwchur.ch>
"""
import logging
import requests
import json

from eWRT.ws.rest import MultiRESTClient

from weblyzard_api.client import (WEBLYZARD_API_URL, WEBLYZARD_API_USER,
                                  WEBLYZARD_API_PASS, OGER_API_URL)
from weblyzard_api.xml_content import XMLContent


logger = logging.getLogger(__name__)

DEFAULT_MAX_RETRY_DELAY = 15
DEFAULT_MAX_RETRY_ATTEMPTS = 5
DAYS_BACK_DEFAULT = 20

# GET URL/{pubmed|pmd}/{txt|bioc|pxml|nxml|pxml.gz}/DOC_ID


class OgerClient(object):
    """
    Provides access to the OntoGene Entity Recognition.

    Currently we support the following types of requests: status, fetch and upload.

    Requests to root are currently not supported since they would simply return an HTML page.

    A fetch request will retrieve an existing document from a known source:   
        GET <BASE_URL>/fetch/<SOURCE>/<OUTPUT_FORMAT>/<DOC_ID>
        POST <BASE_URL>/fetch/<SOURCE>/<OUTPUT_FORMAT>/<DOC_ID>

    An upload request is used to submit a text to be annotated.
        POST <BASE_URL>/upload/<INPUT_FORMAT>/<OUTPUT_FORMAT> [/<DOC_ID>]

    Accepted values:
        SOURCE: pubmed, pmc
        INPUT_FORMAT: txt, bioc, pxml, nxml, pxml.gz
        OUTPUT_FORMAT: bioc, odin, odin_custom, tsv, xml

    """

    ONTOGENE_NS = 'https://pub.cl.uzh.ch/projects/ontogene/medmon-oger/'
    ENTITY_TYPE = 'MedicalEntity'
    DEFAULT_TIMEOUT_SEC = 10

    # available endpoints
    ANNOTATE_PATH = 'upload/txt/bioc_json'
    STATUS_PATH = 'status'

    def __init__(self, url=OGER_API_URL, service_timeout=None):
        """
        :param url: URL of the OGER web service
        :param timeout: optional timeout for service responses
        """
        if isinstance(url, list):
            raise Exception('Oger url cannot be an array')
        if url.endswith('/'):
            url = url[:-1]
        self.url = url
        self.service_timeout = service_timeout
        if self.service_timeout is None:
            self.service_timeout = self.DEFAULT_TIMEOUT_SEC

    def status(self):
        """
        :returns: the status of the OGER web service.
        """
        url = '/'.join([self.url, self.STATUS_PATH])
        return requests.get(url, timeout=self.service_timeout).json()

    """
    def fetch_document(self, docid):

        fetchpath = 'fetch/pubmed/pubtator/' + str(docid)
        r = self.request(path=fetchpath)
        
        return r.json()
    """

    def convert_result(self, result_dict):
        """
        Convert a dict result as produced by the OGER annotation web service.
        :param result_dict: a result from the OGER annotation service, as dict.
        :returns: OGER document converted to Recognyze format.
        """
        result = []
        annotations = []
        try:
            if not 'documents' in result_dict or not len(result_dict['documents']):
                return result

            # this version fixes the offset error
            for passage in result_dict['documents'][0]['passages']:

                for rs in passage['annotations']:
                    start = rs['locations'][0]['offset']
                    end = rs['locations'][0]['offset'] + len(rs['text'])
                    key = self.ONTOGENE_NS + rs['infons']['native_id']
                    ditem = {
                        "key": key,
                        #"resource": rs['infons']['original_resource'],
                        "surfaceForm": rs['text'],  # .encode("utf8")
                        "start": start,
                        "end": end,
                        "confidence": 1,
                        "preferred_name": rs['infons']['preferred_form'],

                        # formerly: rs['infons']['type']
                        "entity_type": self.ENTITY_TYPE,
                        "annotation_type": self.ENTITY_TYPE
                    }
                    annotations.append(ditem)
        except Exception as message:
            logger.error(message)
            raise Exception('Error: {}'.format(message))


        return annotations

    def annotate_text(self, docid, doctext):
        """
        Annotate a document's text content with the OGER annotation service.
        :param docid: the document's ID.
        :param doctext: the document's content to be annotated.
        :returns: OGER annotated document after uploading a text.
        """
        url = '/'.join([self.url, self.ANNOTATE_PATH, docid])
        r = requests.post(url=url, data=doctext.encode(
            'utf-8'), timeout=self.service_timeout)
        if r.status_code == 200:
            return self.convert_result(json.loads(r.content.decode('utf-8')))
        return []
