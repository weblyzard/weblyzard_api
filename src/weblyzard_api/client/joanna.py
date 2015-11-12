'''
Created on Oct 30, 2015

@author: lucas
'''
import logging
import urllib2
import json
import unittest

from time import sleep
from random import random, randint
from eWRT.ws.rest import MultiRESTClient

logger = logging.getLogger('weblyzard_api.client.joanna')
DEFAULT_MAX_RETRY_DELAY = 15
DEFAULT_MAX_RETRY_ATTEMPTS = 5
DAYS_BACK_DEFAULT = 20

WEBLYZARD_API_URL, WEBLYZARD_API_USER, WEBLYZARD_API_PASS = 'http://localhost:8080', '', ''

class PostRequest(object):
    def __init__(self, url, data, headers=[{"Content-Type":"application/json"}]):
        self.url = url
        self.data = json.dumps({"hashes":data})
        self.headers = headers
    def request(self):
        handler = urllib2.HTTPHandler()
        opener = urllib2.build_opener(handler)
        req = urllib2.Request(url=self.url)
        req.add_header("Content-Type","application/json")
        req.get_method = lambda:"POST"
        req.add_data(self.data)
        try:
            conn = opener.open(req)
        except urllib2.URLError, e:
            logger.error("Connection refused.. {}".format(e))
            raise e
        except urllib2.HTTPError, e:
            conn = e
        return conn
        
class Joanna(object):
    """
    Joanna Nilsimsa web service client
    Available endpoints:
        /load/:portalName/:sourceId/:daysBack
            - GET: load the nilsimsa hashes for a portal with sourceId and days back to load
            - Python client function: reload_source_nilsimsa
        /is_similar/:sourceId/:nilsimsaHash
            - Returns true or false for a given nilsimsa hash with a sourceId
            - Python client function: similar_document
        /get_hashes/:sourceId
            - GET: return the list of hashes for a given sourceId
            - Python client function: get_hashes
        /clean_hashes
            - GET: cleans cached hash lists by removing outdated elements and duplicates
            - Python client function: clean_hashes
        /version
            - GET: return the current version of the API
            - Python client function: version
        /status
            - GET: return the status of the API. If functioning it will return "ONLINE" 
            - Python client function: status
        /batchIsSimilar/:portalName/:sourceId/:daysBack
            - POST: make a batch of nilsimsa. If the sourceId isn't present 
                    it will make a /load request instead. The client will 
                    try again to return the batch request. 
            - Returns: 
                Dictionary of hash and similarity {hash:similarity-bool}
                Similarity: False means it is not similar to anythhing with that sourceId
            - Python client function: similar_documents
    Example usage:
        jo = Joanna(url="http://localhost:8080")
    """
    
    def __init__(self, url, default_timeout=None):
        self.url = url
        self.default_timeout = default_timeout
        self.multiRestclient = MultiRESTClient(self.url)

    def get_hashes(self, sourceId, portalName):
        request_url = "get_hashes/{}/{}".format(sourceId, portalName)
        return self.multiRestclient.request(request_url)
    
    def clean_hashes(self):
        request_url = "clean_hashes"
        return self.multiRestclient.request(request_url)
    
    def similar_document(self, sourceId, nilsimsa, portalName):
        request_url = "is_similar/{}/{}/{}".format(sourceId, portalName, nilsimsa)
        return self.multiRestclient.request(request_url)

    def similar_documents(self, sourceId, portalName, nilsimsaList, daysBack=20, max_retry_delay=DEFAULT_MAX_RETRY_DELAY,
        max_retry_attempts=DEFAULT_MAX_RETRY_ATTEMPTS):
        """ Uses PostRequest instead of the eWRT MultiRESTClient for finer control
         of the connection codes for retries
             result: {hash:boolean, ..}
        """
        if daysBack is None:
            daysBack=DAYS_BACK_DEFAULT
            
        if not (sourceId or nilsimsaList):
            logger.error("Arguments missing")
            return
        if isinstance(nilsimsaList, basestring):
            logger.warning("Expected list. Using single instead of batch..")
            return self.similar_document(sourceId, nilsimsaList)
        request_url = "batchIsSimilar/{}/{}/{}".format(portalName, sourceId, daysBack)
        req = PostRequest(self.url + '/' + request_url, nilsimsaList)
        logger.debug('Trying to request: {}'.format(req.url))

        attempts = 0
        conn_code = -1
        while attempts < max_retry_attempts and conn_code != 204:
            conn = req.request()
            conn_code = conn.code
            if conn.code == 200:
                logger.info('successful request')
                data = conn.read()
                if data=="LOADED":
                    logger.info("Nilsimsas loaded from db. Sending request again for results..")
                else:
                    attempts=max_retry_attempts
                    return json.loads(data)
            elif conn.code == 204:
                logger.info('No content found attempts {}'.format(attempts))
                data = conn.read()
                logger.error("No content found.. attempts {} {}".format(
                                                               attempts, data))
            elif conn.code == 400:
                logger.error('Bad request.. 404 error')
                data = conn.read()
                logger.error('Err: {}'.format(data))
            elif conn.code == 500:
                data = conn.read()
                logger.error('Server failure: attempts {} {}'.format(attempts, 
                                                                         data))
                             
            sleep(max_retry_delay * random())
            attempts+=1
            
    def reload_source_nilsimsa(self, sourceId, portal_db, daysBack=20):
        if daysBack is None:
            daysBack = DAYS_BACK_DEFAULT
        request = "load/{}/{}/{}".format(portal_db, sourceId, daysBack)
        return self.multiRestclient.request(request, return_plain=True)
    
    def status(self):
        return self.multiRestclient.request('status', return_plain=True)

    def version(self):
        return self.multiRestclient.request('version', return_plain=True)
    
    def rand_strings(self, num_docs):
        docs_to_send = []
        for _ in xrange(num_docs):
            rand_str = "".join([str(randint(0, 1)) for _ in xrange(256)])
            docs_to_send.append(rand_str)
        return docs_to_send
        
    def stress_test(self, sourceId, portalName, num_docs):
        docs_to_send = self.rand_strings(num_docs)
#         print "Docs to send: {}".format(docs_to_send)
        results = self.similar_documents(sourceId, portalName, docs_to_send)
        print "Results {}".format(results)

class JoannaTest(unittest.TestCase):
    
    def setUp(self):
        self.joanna = Joanna(url="http://localhost:9000/joanna")
        self.docs = 10
        self.rand_strings = self.joanna.rand_strings(self.docs)
        self.source_id = 21555
        self.test_db = 'test_weblyzard'

    def test_random_strings(self):
        self.assertEqual(len(self.rand_strings), 10)
#     
    def test_online(self):
        self.assertEqual(self.joanna.status(), '"ONLINE"')
    
    def test_batch_request(self):
        batch_results = self.joanna.similar_documents(self.source_id, self.test_db, self.rand_strings, 20)
        for nilsimsa, similar in batch_results.iteritems():
            self.assertEqual(similar, 'false')
        batch_results = self.joanna.similar_documents(self.source_id, self.test_db, self.rand_strings, 20)
        for nilsimsa, similar in batch_results.iteritems():
            self.assertEqual(similar, 'true')
        
    def test_single_request(self):
        self.rand_strings = self.joanna.rand_strings(self.docs)
        single_result = self.joanna.similar_document(self.source_id, self.rand_strings[0], self.test_db)
        self.assertEqual(single_result, False)
        single_result = self.joanna.similar_document(self.source_id, self.rand_strings[0], self.test_db)
        self.assertEqual(single_result, True)
     
    def test_loaded(self):
        loaded_result = self.joanna.reload_source_nilsimsa(self.source_id, self.test_db, 20)
        self.assertEqual(loaded_result, 'LOADED')
    
    def test_existing_document(self):
        existing_doc = '1100101100100110001001110011001000000010001000001010100001001110100010000001001110110010101100111101000011000100100101110010000100001111011011100001101110100001100101011011001001001100100011000110100001000001101111100101001011100010010100101111010001001011'
        single_result = self.joanna.similar_document(self.source_id, existing_doc, self.test_db)
        self.assertEqual(single_result, True)
        batch_result = self.joanna.similar_documents(self.source_id, self.test_db, [existing_doc])
        for nilsimsa, similar in batch_result.iteritems():
            self.assertEqual(similar, 'true')
            
if __name__ == '__main__':    
    unittest.main()
