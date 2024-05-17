#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This module provides a python client for the WLT REST API.

.. moduleauthor: Max Göbel <goebel@weblzyard.com>
"""
from __future__ import unicode_literals

import json
import requests

from typing import List, Dict

import logging
logger = logging.getLogger(__name__)


class WltApiClient(object):

    TOKEN_ENDPOINT = 'token'

    BASE_URL = 'https://api.weblyzard.com'
    API_VERSION = '1.0'

    def __init__(self, base_url: str=BASE_URL,
                 version: float=API_VERSION,
                 username: str=None, password: str=None):
        """
        Constructor.
        """
        if base_url.endswith(f'/{version}'):
            base_url = base_url.replace(f'/{version}', '')
        self.base_url = base_url
        self.version = version
        self.username = username
        self.password = password
        self.auth_token = None
        self.auth_token = self.get_auth_token(self.username, self.password)

    def get_auth_token(self, username: str, password: str) -> str:
        """ 
        GET a valid authentication token from the server. 
        :param username, as provided by webLyzard
        :param password, as provided by webLyzard
        """
        if self.auth_token:
            return self.auth_token
        url = '/'.join([self.base_url, self.version, self.TOKEN_ENDPOINT])
        r = requests.get(url, auth=(username, password))
        if r.status_code == 200:
            return r.content.decode('utf-8')
        return r


class WltSearchRestApiClient(WltApiClient):
    """
    The client for the WL Search REST API.
    `Documentation <https://api.weblyzard.com/doc/ui/#!/Search_API>`_
    """
    DOCUMENT_ENDPOINT = 'search/'
    KEYWORD_ENDPOINT = 'keyentities/'
    ENTITIES_ENDPOINT = 'entities/'

    def search_documents(self, sources: List[str], terms: List[str]=None,
                         entities: List[str]=None,
                         auth_token: str=None, content_id: int=None,
                         start_date: str=None, end_date: str=None,
                         count: int=10, offset: int=0, source_ids: int=None,
                         max_docs: int=-1, exact_match: bool=True,
                         similarity: int=70,
                         fields: List[str]=['document.contentid']):
        """ 
        Search an index for documents matching the search parameters.
        :param sources: required sources where to look for content.
        :param content_id: optional single content_id .
        :param terms: optional list of terms to filter for.
        :param entities: optional list of entity URIs to filter for.
        :param source_ids: optional source_ids to filter by.
        :param auth_token: the webLyzard authentication token, if any.
        :param start_date: result documents must be younger than this, if given (e.g. \"2018-08-01\")
        :param end_date: result documents must be older than this, if given
        :param count: number of documents to return, default 10
        :param offset: offset to search (use with combination with count and hints)
        :param fields: list of fields of document to return, default just contentid
        :returns: The result documents as serialized JSON
        :rtype: str
        """
        if not auth_token:
            auth_token = self.auth_token
        if isinstance(auth_token, bytes):
            auth_token = auth_token.decode('utf-8')

        assert auth_token is not None

        if max_docs is None:
            max_docs = 1000

        if not isinstance(sources, list):
            sources = [sources]
        query = {
            "sources": sources,
            "fields": fields,
            # could change this later, not necessary for compute task
            # "query": "<<query>>",
            "count": count,
            "offset": offset
        }

        term_query = {}
        entity_query = {}
        if content_id is not None and isinstance(content_id, int):
            # construct an ID query
            term_query.update(
                {
                    "contentid": {
                        "eq": content_id
                    }
                })
            max_docs = 1

        if source_ids is not None:
            if not isinstance(source_ids, list):
                source_ids = [source_ids]

            # construct an ID query
            term_query.update(
                {
                    "source_identifier": {
                        "terms": source_ids
                    }
                })
        if entities is not None and isinstance(entities, list):
            entity_query = {
               "entity": {
                   "key": entities[0]
                }
            }
        if terms is not None:
            # construct a term query

            term_query.update(
                {
                    "bool": {
                        "should": []
                    }
                })
            for term in terms:
                if exact_match:
                    term_query["bool"]["should"].append(
                        {"text": {
                            "phrase": term
                        }})
                else:
                    term_query["bool"]["should"].append(
                        {"text": {
                            "similarto": {"value": term,
                                          "options": {
                                              "minmatching": {
                                                  "percent": similarity}}}
                        }})

        # date filters for term queries
        if start_date:
            query["beginDate"] = str(start_date)

        if end_date:
            query["endDate"] = str(end_date)

        if entity_query is not None and len(entity_query):
            query["query"] = entity_query

        if term_query is not None and len(term_query):
            query["filter"] = term_query

        headers = {'Authorization': 'Bearer %s' % auth_token,
                   'Content-Type': 'application/json'}
        url = '/'.join([self.base_url, self.version, self.DOCUMENT_ENDPOINT])

        result_count = 0
        total = 1
        r = None

        while result_count < total:
            query["offset"] = result_count
            squery = json.dumps(query)
            r = requests.post(url, data=squery, headers=headers)
            try:

                if r.status_code == 200:
                    response = json.loads(r.content)['result']
                    total = response.get('total', 0)
                    if max_docs > 0:
                        total = max_docs
                    hits = response.get('hits', [])
                    if len(hits) > 0:
                        result_count += len(hits)
                        yield hits
                    else:
                        return r
                else:
                    return r
            except Exception as e:
                logger.error("Accessing: %s : %s - %s", url, squery, e,
                             exc_info=True)
                return r

        return r

    def search_keywords(self, sources: List[str], start_date: str, end_date: str,
                        num_keywords: int=5, num_associations: int=0,
                        auth_token: str=None, terms: List[str]=None,
                        entities: List[str]=None):
        """ 
        Search an index for top keyword associations matching the search parameters.
        :param sources: required sources where to look for content
        :param terms: the query string
        :param entities: optional entities for filtering
        :param start_date: result documents must be younger than this (e.g. \"2018-08-01\")
        :param end_date: result documents must be older than this
        :param num_keywords: how many keywords to return
        :param num_associations: how many keyword associations to return
        :param auth_token: the webLyzard authentication token, if any
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
        # construct a term query
        if terms is not None:
            term_query = {
                "filter": []
            }
            for term in terms:
                term_query["filter"].append(term)

            query["query"] = term_query

            query = query.replace(',<<term_query>>', term_query)
        else:
            query = query.replace(',<<term_query>>', '')
        query = json.loads(query)

        # additionally return keyword counts
        fields = ["keyword.count", "keyword.key", "keyword.name"]
        if num_associations:
            # also return associations per keyword
            fields.append("keyword.associations")

        data = dict(sources=sources, query=query, count=num_keywords,
                    associations=num_associations,
                    fields=fields)
        data = json.dumps(data)
        headers = {'Authorization': 'Bearer %s' % auth_token,
                   'Content-Type': 'application/json'}
        url = '/'.join([self.base_url, self.version, self.KEYWORDS_ENDPOINT])
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

    def search_entities(self, sources: List[str], start_date: str, end_date: str,
                        count: int=5, entity_types: List[str]=None,
                        fields: List[str]=None,
                        auth_token: str=None, terms: List[str]=None):
        """ 
        Search an index for top entities matching the search parameters.
        :param sources: required sources where to look for content.
        :param term_query: the query string
        :param start_date: result documents must be younger than this (e.g. \"2018-08-01\")
        :param end_date: result documents must be older than this
        :param count: how many entities to return
        :param entity_types: what entity types to return
        :param auth_token: the webLyzard authentication token, if any
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
        # construct a term query
        if terms is not None:
            term_query = {
                "filter": []
            }
            for term in terms:
                term_query["filter"].append(term)

            query["query"] = term_query

            query = query.replace(',<<term_query>>', term_query)
        else:
            query = query.replace(',<<term_query>>', '')
        query = json.loads(query)

        # additionally return keyword counts
        if fields is None:
            fields = []
        fields.extend(["keyword.count", "keyword.key", "keyword.name"])

        data = dict(sources=sources, query=query, count=count,
                    entityTypes=entity_types,
                    fields=fields)
        data = json.dumps(data)
        headers = {'Authorization': 'Bearer %s' % auth_token,
                   'Content-Type': 'application/json'}
        url = '/'.join([self.base_url, self.version, self.ENTITIES_ENDPOINT])
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


class WltMesaApiClient(WltApiClient):
    """
    The client for the WL Mesa REST API.
    """
    ENDPOINT = 'mesa/entities'

    def get(self, auth_token: str=None):
        """ """
        if not auth_token:
            auth_token = self.auth_token
        headers = {'Authorization': 'Bearer %s' % auth_token,
                   'Content-Type': 'application/json'}
        url = '/'.join([self.base_url, self.ENDPOINT])
        try:
            r = requests.get(url, headers=headers)
            if r.status_code == 200:
                return json.loads(r.content)['result']
        except Exception as e:
            logger.error(
                "Accessing: {} : {}".format(url, e), exc_info=True)
            return r
        return r

    def post(self, data: Dict, auth_token: str=None):
        """ """
        if auth_token is None:
            auth_token = self.auth_token
        data = json.dumps(data)
        headers = {'Authorization': 'Bearer %s' % auth_token,
                   'Content-Type': 'application/json'}
        url = '/'.join([self.base_url, self.ENDPOINT])
        try:
            r = requests.post(url,
                              data=data,
                              headers=headers)
            if r.status_code == 201:
                return json.loads(r.content)
        except Exception as e:
            logger.error(
                "Accessing: {} : {} - {}".format(url, data, e), exc_info=True)
            return r
        return r
