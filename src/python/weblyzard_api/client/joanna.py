'''
Created on Oct 30, 2015

@author: lucas
'''
import logging
import urllib2
import json

from time import sleep
from random import random, randint

from eWRT.ws.rest import MultiRESTClient

logger = logging.getLogger('weblyzard_api.client.joanna')
DEFAULT_MAX_RETRY_DELAY = 15
DEFAULT_MAX_RETRY_ATTEMPTS = 5
DAYS_BACK_DEFAULT = 20


class PostRequest(object):
    ''' Make a post request and return the connection without
    reading the data. Allows for finer handling of error codes
    '''
    def __init__(self, url, data):
        self.url = url
        self.data = json.dumps({"hashes": data})
        self.headers = [{"Content-Type": "application/json"}]
    
    def request(self):
        handler = urllib2.HTTPHandler()
        opener = urllib2.build_opener(handler)
        req = urllib2.Request(url=self.url)
        req.add_header("Content-Type", "application/json")
        req.get_method = lambda: "POST"
        req.add_data(self.data)
        try:
            conn = opener.open(req)
        except urllib2.HTTPError, e:
            conn = e
        except urllib2.URLError, e:
            logger.error("Connection refused.. %s", e)
            raise e
        return conn
        

class Joanna(object):
    """
    Joanna Nilsimsa web service client
    Available endpoints:
        /load/:portalName/:sourceId/:daysBack
            - GET: load the nilsimsa hashes for a portal with sourceId 
              and days back to load
            - Python client function: reload_source_nilsimsa
        /is_similar/:sourceId/:nilsimsaHash
            - Returns true or false for a given nilsimsa hash 
              with a sourceId
            - Python client function: similar_document
        /get_hashes/:sourceId
            - GET: return the list of hashes for a given sourceId
            - Python client function: get_hashes
        /clean_hashes
            - GET: cleans cached hash lists by removing outdated 
              elements and duplicates
            - Python client function: clean_hashes
        /version
            - GET: return the current version of the API
            - Python client function: version
        /status
            - GET: return the status of the API. 
              If functioning it will return "ONLINE" 
            - Python client function: status
        /batchIsSimilar/:portalName/:sourceId/:daysBack
            - POST: make a batch of nilsimsa. If the sourceId isn't
               present it will make a /load request instead. 
               The client will try again to return the batch request. 
            - Returns: 
                Dictionary of hash and similarity 
                {hash:similarity-bool}
                Similarity: False means it is not similar to 
                anything with that sourceId
            - Python client function: similar_documents
    Example usage:
        jo = Joanna(url="http://localhost:8080")
    """
    
    def __init__(self, url, default_timeout=None):
        self.url = url
        self.default_timeout = default_timeout
        self.multiRestclient = MultiRESTClient(self.url)

    def get_hashes(self, sourceId, portalName):
        ''' Return the hashes for a specific source and portal
        '''
        request_url = "get_hashes/{}/{}".format(sourceId, portalName)
        return self.multiRestclient.request(request_url)
    
    def clean_hashes(self):
        ''' Make a request to clean old nilsimsa hashes
        '''
        request_url = "clean_hashes"
        return self.multiRestclient.request(request_url)
    
    def similar_document(self, sourceId, nilsimsa, portalName, 
                         daysBack=None):
        ''' Get the similarity of a single document. 
        Expected response: Boolean True or False 
        '''
        if daysBack is None:
            daysBack = 20
        request_url = "is_similar/{}/{}/{}/{}".format(
                    sourceId, portalName, nilsimsa, daysBack)
        
        result = self.multiRestclient.request(
                request_url, return_plain=True)
        if result == "LOADED":
            result = self.multiRestclient.request(
                    request_url, return_plain=True)
        else:
            return result

    def similar_documents(self, sourceId, portalName, nilsimsaList,
                          daysBack=20):
        """ Uses PostRequest instead of the eWRT MultiRESTClient 
         for finer control of the connection codes for retries
             result: {hash:boolean, ..}
        """
        max_retry_delay = DEFAULT_MAX_RETRY_DELAY
        max_retry_attempts = DEFAULT_MAX_RETRY_ATTEMPTS
        if daysBack is None:
            daysBack = DAYS_BACK_DEFAULT
            
        if not (sourceId or nilsimsaList):
            logger.error("Arguments missing")
            return
        if isinstance(nilsimsaList, basestring):
            logger.error("Expected list. Please use single_document")
            raise ValueError('Expected a list')

        request_url = "batchIsSimilar/{}/{}/{}".format(
                                    portalName, sourceId, daysBack)
        req = PostRequest(self.url + '/' + request_url, nilsimsaList)
        logger.debug('Trying to request: %s', req.url)

        attempts = 0
        conn_code = -1

        while attempts < max_retry_attempts and conn_code != 204:
            conn = req.request()
            conn_code = conn.code
            if conn.code == 200:
                logger.info('successful request')
                data = conn.read()
                if data == "LOADED":
                    logger.info("Nilsimsas loaded from db. \
                    Sending request again for results..")
                else:
                    attempts = max_retry_attempts
                    return json.loads(data)
            elif conn.code == 204:
                logger.info('No content found attempts %d', attempts)
                data = conn.read()
            elif conn.code == 400:
                logger.error('Bad request.. 404 error')
                data = conn.read()
                logger.error('Err: %s', data)
            elif conn.code == 500:
                data = conn.read()
                logger.error(
                    'Server failure: attempts %d %s', attempts, data)
            sleep(max_retry_delay * random())
            attempts += 1
            
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
    
