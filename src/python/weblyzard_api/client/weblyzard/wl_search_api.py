#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Oct 29, 2019

.. codeauthor:: Max Göbel <goebel@weblyzard.com>
"""
import json
import requests
import logging

from weblyzard_api.client.weblyzard import WlAuthenticatedApi

logger = logging.getLogger('weblyzard_api.client.wl_search_rest_api_client')


class WlSearchApiClient(WlAuthenticatedApi):
    """
    The client for the WL Search REST API.
    `Documentation <https://api.weblyzard.com/doc/ui/#!/Search_API>`_
    """
    DOCUMENT_ENDPOINT = 'search/'
    KEYWORD_ENDPOINT = 'rest/com.weblyzard.api.search/keywords'

    def search_documents(self, sources, term_query, auth_token=None,
                         start_date=None, end_date=None, count=10, offset=0,
                         fields=['document.contentid']):
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

        query = json.dumps(query)

        if isinstance(term_query, dict):
            term_query = json.dumps(term_query)

        data = query.replace('"<<query>>"', term_query)
        headers = {'Authorization': 'Bearer %s' % auth_token,
                   'Content-Type': 'application/json'}
        url = '/'.join([self.base_url, self.DOCUMENT_ENDPOINT])
        r = requests.post(url,
                          data=data,
                          headers=headers)
        if r.status_code == 200:
            return json.loads(r.content)['result']
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
        url = '/'.join([self.base_url, self.KEYWORD_ENDPOINT])
        r = requests.post(url,
                          data=data,
                          headers=headers)
        if r.status_code == 200:
            return json.loads(r.content)['result']
        return r
