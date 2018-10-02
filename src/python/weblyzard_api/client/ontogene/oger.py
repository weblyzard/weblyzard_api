#!/usr/bin/python
# -*- coding: utf8 -*-
'''
.. moduleauthor:: Adrian Brasoveanu <adrian.brasoveanu@htwchur.ch>
'''
import logging

from eWRT.ws.rest import MultiRESTClient

from weblyzard_api.client import (WEBLYZARD_API_URL, WEBLYZARD_API_USER,
                                  WEBLYZARD_API_PASS)
from weblyzard_api.xml_content import XMLContent

INTERNAL_PROFILE_PREFIX = 'extras.'
LOGGER = logging.getLogger('weblyzard_api.client.ontogene.oger')

DEFAULT_MAX_RETRY_DELAY = 15
DEFAULT_MAX_RETRY_ATTEMPTS = 5
DAYS_BACK_DEFAULT = 20

#GET URL/{pubmed|pmd}/{txt|bioc|pxml|nxml|pxml.gz}/DOC_ID

class SpecialGetRequest(object):
    ''' Make a post request and return the connection without
    reading the data. Allows for finer handling of error codes
    '''
    def __init__(self, url, data):
        self.url = url
        #self.data = json.dumps({"hashes": data})
        #self.headers = [{"Content-Type": "application/json"}]
    
    def request(self):
        handler = urllib2.HTTPHandler()
        opener = urllib2.build_opener(handler)
        req = urllib2.Request(url=self.url)
        req.add_header("Content-Type", "application/json")
        req.get_method = lambda: "GET"
        req.add_data(self.data)
        try:
            conn = opener.open(req)
        except urllib2.HTTPError as e:
            conn = e
        except urllib2.URLError as e:
            logger.error("Connection refused.. %s", e)
            raise e
        return conn


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
    
    def status(self):
        '''
        :returns: the status of the OGER web service.
        '''
        return self.request(path='status')

    def fetch_document(self, docid='29630699'):
        '''
        :returns: OGER annotated document from pubmed or DB.
        '''
        #fetch/pubmed/tsv/29630699
        fetchpath = '/fetch/'+'pubmed' + '/bioc_json/' + docid
        r = self.request(path=fetchpath)
        
        #print(r.status())
        return r.json()
        #print(r.status())
        #print(r.json())
        #raise NotImplementedError
        

    def convert_document(self, oger_json):
        '''
        :returns: OGER document converted to Recognyze format.
        '''
        res = oger_json

        entities = {}
        d2 = []
        for passage in res['documents'][0]['passages']:
        
            for rs in passage['annotations']:
                print(rs)
                start = rs['locations'][0]['offset']
                end = rs['locations'][0]['offset'] + len(rs['text'])
                ditem = {
                    "key": rs['infons']['original_id'],
                    "resource": rs['infons']['original_resource'],
                    "surfaceForm": rs['text'], #.encode("utf8")
                    "start": start,
                    "end": end,
                    "confidence": 1,
                    "preferred_name": rs['infons']['preferred_form'],
                    "entity_type": rs['infons']['type'],
                    "entity_metadata": {
                        "document_indexes": [
                            start,
                            end
                            ]
                        }
                }
            #print(ditem)         
            d2.append(ditem)
        return d2
    
    def upload_document(self, docid, doctext):
        '''
        :returns: OGER annotated document after uploading a text.
        '''
        url = "https://pub.cl.uzh.ch/projects/ontogene/oger/upload/txt/bioc_json"
        files = {'file1': (docid, doctext)}
        
        r = requests.post(url, files=files)
        print(r.text)
        
        res = r.json()
        return convert_document(res)
        #raise NotImplementedError
    
    def search_documents(self):
        '''
        :returns: the status of the Recognize web service.
        '''
        raise NotImplementedError
    