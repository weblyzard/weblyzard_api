#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This module provides a python client for the WLT REST API.

.. moduleauthor: Max Göbel <goebel@weblzyard.com>
"""
from __future__ import unicode_literals

import json
import requests
import logging

logger = logging.getLogger(__name__)


class WltApiClient(object):

    TOKEN_ENDPOINT = 'token'

    BASE_URL = 'http://api.weblyzard.com'
    API_VERSION = 1.0

    def __init__(self, base_url:str=BASE_URL,
                 version:float=API_VERSION,
                 username:str=None, password:str=None):
        self.base_url = base_url
        self.version = version
        self.username = username
        self.password = password
        self.auth_token = self.get_auth_token(self.username, self.password)

    def get_auth_token(self, username, password):
        """ 
        GET a valid authentication token from the server. 
        :param username, as provided by webLyzard
        :param password, as provided by webLyzard
        """
        url = '/'.join([self.base_url, self.TOKEN_ENDPOINT])
        r = requests.get(url, auth=(username, password))
        if r.status_code == 200:
            return r.content
        return r


class WltSearchRestApiClient(WltApiClient):
    """
    The client for the WL Search REST API.
    `Documentation <https://api.weblyzard.com/doc/ui/#!/Search_API>`_
    """
    DOCUMENT_ENDPOINT = 'search/'
    KEYWORD_ENDPOINT = 'rest/com.weblyzard.api.search/keywords'

    def search_documents(self, sources, term_query, auth_token=None,
                         start_date=None, end_date=None, count=10, offset=0,
                         max_docs=-1, fields=['document.contentid']):
        """ 
        Search an index for documents matching the search parameters.
        :param sources
        :param term_query, the query string
        :param auth_token, the webLyzard authentication token, if any
        :param start_date, result documents must be younger than this, if given (e.g. \"2018-08-01\")
        :param end_date, result documents must be older than this, if given
        :param count, number of documents to return, default 10
        :param offset, offset to search (use with combination with count and hints)
        :param fields, list of fields of document to return, default just contentid
        :returns: The result documents as serialized JSON
        :rtype: str
        """
        assert len(term_query)

        if not auth_token:
            auth_token = self.auth_token
        if isinstance(auth_token, bytes):
            auth_token = auth_token.decode('utf-8')

        assert auth_token is not None

        if not isinstance(sources, list):
            sources = [sources]
        query = {
            "sources": sources,
            "fields": fields,
            # could change this later, not necessary for compute task
            "query": "<<query>>",
            "count": count,
            "offset": offset
        }
        if start_date:
            query["beginDate"] = str(start_date)

        if end_date:
            query["endDate"] = str(end_date)

        query["query"] = term_query
        headers = {'Authorization': 'Bearer %s' % auth_token,
                   'Content-Type': 'application/json'}
        url = '/'.join([self.base_url, self.DOCUMENT_ENDPOINT])

        result_count = 0
        total = 1

        while result_count < total:
            query["offset"] = result_count
            squery = json.dumps(query)
            r = requests.post(url, data=squery, headers=headers)
            try:
                if r.status_code == 200:
                    response = json.loads(r.content)['result']
                    total = response['total']
                    if max_docs > 0:
                        total = max_docs
                    hits = response['hits']
                    result_count += len(hits)
                    yield hits
                else:
                    return r
            except Exception as e:
                logger.error("Accessing: %s : %s - %s", url, squery, e,
                             exc_info=True)
                return r

        return r

    def search_keywords(self, sources, start_date, end_date, num_keywords=5,
                        num_associations=5, auth_token=None, term_query=""):
        """ 
        Search an index for top keyword associations matching the search parameters.
        :param sources
        :param term_query, the query string
        :param start_date, result documents must be younger than this (e.g. \"2018-08-01\")
        :param end_date, result documents must be older than this
        :param num_keywords, how many keywords to return
        :param num_associations, how many keyword associations to return
        :param auth_token, the webLyzard authentication token, if any
        :returns: The result documents as serialized JSON
        :rtype: str
        """
        if not auth_token:
            auth_token = self.auth_token
        if not isinstance(sources, list):
            sources = [sources]
        query = """{"bool" : {
                          "must" : [
                            {
                              "date" : {
                                "gte":"%s",
                                "lte":"%s"
                              }
                            },<<term_query>>
                          ]
                        }}
        """ % (start_date, end_date)
        if len(term_query) > 0:
            term_query = ',%s' % term_query
        query = query.replace(',<<term_query>>', term_query)
        query = json.loads(query)
        data = dict(sources=sources, query=query, count=num_keywords,
                    associations=num_associations)
        data = json.dumps(data)
        headers = {'Authorization': 'Bearer %s' % auth_token,
                   'Content-Type': 'application/json'}
        url = '/'.join([self.base_url, self.version, self.KEYWORD_ENDPOINT])
        try:
            r = requests.post(url,
                              data=data,
                              headers=headers)
            if r.status_code == 200:
                return json.loads(r.content)['result']
        except Exception as e:
            logger.error(
                "Accessing: {} : {} - {}".format(url, data, e), exc_info=True)
            return r
        return r


class WltDocumentRestApiClient(WltApiClient):

    def create_documents(self, documents) -> bool:
        pass

    def update_document(self, content_id:int, update:dict) -> bool:
        pass

    def delete_document(self, content_id:int) -> bool:
        pass

    def retrieve_document(self, content_id:int) -> dict:
        pass


class WltStatisticsRestApiClient(WltApiClient):

    def create_observations(self, observations) -> bool:
        pass

    def update_observation(self, observation_id:int, update:dict) -> bool:
        pass

    def delete_observation(self, observation_id:int) -> bool:
        pass

    def retrieve_observation(self, observation_id:int) -> dict:
        pass
