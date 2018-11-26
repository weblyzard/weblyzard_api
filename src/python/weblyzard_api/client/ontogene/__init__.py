#!/usr/bin/python
# -*- coding: utf8 -*-
'''
.. moduleauthor:: Adrian Brasoveanu <adrian.brasoveanu@htwchur.ch>
'''
import logging
import requests

from eWRT.ws.rest import MultiRESTClient

from weblyzard_api.client import (WEBLYZARD_API_URL, WEBLYZARD_API_USER,
                                  WEBLYZARD_API_PASS, OGER_API_URL)
from weblyzard_api.xml_content import XMLContent

INTERNAL_PROFILE_PREFIX = 'extras.'
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
        print(res)      
        result = []
        
        try:
            #TODO: talk to OGER developers to fix this rather than have it fixed here!
            #this is a fix for offset which always seems to be delayed with this value
            offset = res['documents'][0]['passages'][1]['annotations'][0]['locations'][0]['offset']
            
            for passage in res['documents'][0]['passages']:
            
                for rs in passage['annotations']:
                    start = rs['locations'][0]['offset']
                    end = rs['locations'][0]['offset'] + len(rs['text'])
                    ditem = {
                        "key": rs['infons']['original_id'],
                        #"resource": rs['infons']['original_resource'],
                        "surfaceForm": rs['text'], #.encode("utf8")
                        #includes fixes for offset
                        "start": start - offset,
                        "end": end - offset,
                        "offset": offset,
                        "confidence": 1,
                        "preferred_name": rs['infons']['preferred_form'],
                        "entity_type": rs['infons']['type']
                    }
                    result.append(ditem)
        except Exception as e:
            message = e
            logger.error(message)
            raise Exception('Span error: {}'.format(message))
        print(result)
        return result
    
    def annotate_text(self, docid, doctext):
        '''
        :returns: OGER annotated document after uploading a text.
        '''
        url = OGER_API_URL + "upload/txt/bioc_json"
        files = {'file1': (docid, doctext)}
        headers = {'content-type' : 'text/plain'}
        
        r = requests.post(url, files=files, headers=headers)
        res = r.json()
        return self.convert_document(res)
    