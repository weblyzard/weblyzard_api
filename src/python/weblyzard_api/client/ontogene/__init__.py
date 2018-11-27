#!/usr/bin/python
# -*- coding: utf8 -*-
'''
.. moduleauthor:: Adrian Brasoveanu <adrian.brasoveanu@htwchur.ch>
'''
import logging
import requests
import json

from eWRT.ws.rest import MultiRESTClient

from weblyzard_api.client import (WEBLYZARD_API_URL, WEBLYZARD_API_USER,
                                  WEBLYZARD_API_PASS, OGER_API_URL)
from weblyzard_api.xml_content import XMLContent

ONTOGENE_NS = 'https://pub.cl.uzh.ch/projects/ontogene/medmon-oger/'

LOGGER = logging.getLogger('weblyzard_api.client.ontogene.oger')

DEFAULT_MAX_RETRY_DELAY = 15
DEFAULT_MAX_RETRY_ATTEMPTS = 5
DAYS_BACK_DEFAULT = 20

#GET URL/{pubmed|pmd}/{txt|bioc|pxml|nxml|pxml.gz}/DOC_ID

class Oger(MultiRESTClient):
    '''
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

    '''
    def __init__(self, url=OGER_API_URL, default_timeout=None):
        '''
        :param url: URL of the jeremia web service
        #:param usr: optional user name
        #:param pwd: optional password
        '''
        self.url = OGER_API_URL
        
    def status(self):
        '''
        :returns: the status of the OGER web service.
        '''
        #return self.request(path='status')
        url = OGER_API_URL + "status"
        r = requests.get(url)
        result = r.json()
        return result

    
    '''
    def fetch_document(self, docid):

        fetchpath = 'fetch/pubmed/pubtator/' + str(docid)
        r = self.request(path=fetchpath)
        
        return r.json()
    '''

    def convert_document(self, oger_json):
        '''
        :returns: OGER document converted to Recognyze format.
        '''
        res = oger_json  
        result = []
        
        try:
            #this version fixes the offset error         
            for passage in res['documents'][0]['passages']:
            
                for rs in passage['annotations']:
                    start = rs['locations'][0]['offset']
                    end = rs['locations'][0]['offset'] + len(rs['text'])
                    key = ONTOGENE_NS + rs['infons']['original_id']
                    ditem = {
                        "key": key,
                        #"resource": rs['infons']['original_resource'],
                        "surfaceForm": rs['text'], #.encode("utf8")
                        "start": start,
                        "end": end,
                        "confidence": 1,
                        "preferred_name": rs['infons']['preferred_form'],
                        "entity_type": rs['infons']['type']
                    }
                    result.append(ditem)
        except Exception as e:
            message = e
            LOGGER.error(message)
            raise Exception('Error: {}'.format(message))

        return result
    
    def annotate_text(self, docid, doctext):
        '''
        :returns: OGER annotated document after uploading a text.
        '''
        url = OGER_API_URL + "upload/txt/bioc_json/" + docid
        r = requests.post(url=url, data=doctext.encode('utf-8'))
        if r.status_code == 200:
            return self.convert_document(json.loads(r.content.decode('utf-8')))
        else:
            return None
    