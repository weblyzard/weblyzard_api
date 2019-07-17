#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This module provides an easy client for the WL Document REST API.

    .. moduleauthor: Fabian Fischer <fabian.fischer@modul.ac.at>
"""

import json
import requests


class WlComputeRestApiClient(object):
    """
    The client for the WL Compute REST API.
    """
    API_VERSION = 0.1

    ENDPOINT_STATUS = 'status'

    ENDPOINT_REGISTER_COMPLETED_CONTENT_IDS = 'completed_cids'

    ENDPOINT_REGISTER_REQUIRED_CONTENT_IDS = 'register_required_cids'

    ENDPOINT_NEW_TASKS = 'new'

    ENDPOINT_TASK_STATUS = 'task'

    def __init__(self, base_url):
        """
        Sets the base url for the API endpoint.

        :param base_url: The base URL without version number.
        :type base_url: str
        """
        self.base_url = '/'.join([base_url, str(self.API_VERSION)])

    def register_completed_content_ids(self, task_id, content_ids):
        """
        Adds the document to the given portal.

        :param task_id: The task_id of the task processed.
        :type task_id: str
        :param content_ids: A list of content_ids that have finished for a task_id.
        :type content_ids: list
        :returns: True if registration succeeded, False otherwise.
        :rtype: str
        """
        payload = json.dumps(content_ids)
        r = requests.post('/'.join([self.base_url,
                                    self.ENDPOINT_REGISTER_COMPLETED_CONTENT_IDS,
                                    task_id]),
                          data=payload,
                          headers={'Content-Type': 'application/json'})
        return r.json()

    def register_required_content_ids(self, task_id, content_ids):
        """
        Registers a list of content_ids as requirement for task completion.

        :param task_id: The task_id of the task processed.
        :type task_id: str
        :param content_ids: A list of content_ids that must finish for a task_id to be completed.
        :type content_ids: list
        :returns: True if registration succeeded, False otherwise.
        :rtype: str
        """
        payload = json.dumps(content_ids)
        r = requests.post('/'.join([self.base_url,
                                    self.ENDPOINT_REGISTER_REQUIRED_CONTENT_IDS,
                                    task_id]),
                          data=payload,
                          headers={'Content-Type': 'application/json'})
        return r.json()

    def retrieve_task(self, task_id):
        """
        Retrieve the status of a task by IDs.

        :param task_id: The task_id of the task to retrieve.
        :type task_id: str
        :rtype: str
        """
        r = requests.get('/'.join([self.base_url, self.ENDPOINT_TASK_STATUS,
                                   str(task_id)]))
        return r.json()

    def status(self):
        """
        Retrieve the status the compute API service.

        :rtype: str
        """
        r = requests.get('/'.join([self.base_url, self.ENDPOINT_STATUS]))
        return r.json()


class WlSearchRestApiClient(object):
    """
    The client for the WL Search REST API.
    `Documentation <https://api.weblyzard.com/doc/ui/#!/Search_API>`_
    """
    DOCUMENT_ENDPOINT = 'rest/com.weblyzard.api.search/'
    KEYWORD_ENDPOINT = 'rest/com.weblyzard.api.search/keywords'
    TOKEN_ENDPOINT = 'token'

    def __init__(self, base_url, username, password):
        self.base_url = base_url
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

    def search_documents(self, sources, term_query, auth_token=None,
                         start_date=None, end_date=None):
        """ 
        Search an index for documents matching the search parameters.
        :param sources
        :param term_query, the query string
        :param auth_token, the webLyzard authentication token, if any
        :param start_date, result documents must be younger than this, if given (e.g. \"2018-08-01\")
        :param end_date, result documents must be older than this, if given
        :returns: The result documents as serialized JSON
        :rtype: str
        """
        assert len(term_query)

        if not auth_token:
            auth_token = self.auth_token

        assert auth_token is not None

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

        term_query = ',%s' % term_query
        query = query.replace(',<<term_query>>', term_query)
        query = json.loads(query)
        data = dict(sources=sources, query=query)
        data = json.dumps(data)
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


class WlStatisticsRestApiClient(object):
    """
    The client for the WL Statistics REST API.
    `Documentation <https://api.weblyzard.com/doc/ui/#!/Statistical_Data_API>`_

    """
    API_VERSION = 2.0

    PATH = 'observations'

    def __init__(self, base_url):
        """
        Sets the base url for the API endpoint.

        :param base_url: The base URL without version number.
        :type base_url: str
        """
        self.base_url = '/'.join([base_url, str(self.API_VERSION)])

    def add_observation(self, repository_name, observation, indicator_id):
        """
        Adds the document to the given portal.

        :param repository_name: The repository to add the observation to.
        :type repository_name: str
        :param observation: The observation to add. Either as JSON structure \
                or as dict corresponding to the JSON format.
        :type observation: str or dict
        :returns: The id of the added observation.
        :rtype: int
        """
        if isinstance(observation, dict):
            observation = json.dumps(observation)
        r = requests.post('/'.join([self.base_url, self.PATH,
                                    repository_name, indicator_id]),
                          data=observation,
                          headers={'Content-Type': 'application/json'})
        return r.json()

    def retrieve_observation(self, repository_name, observation_id):
        """
        Retrieve the observation with id from portal_name.

        :param repository_name: The repository of the observation
        :type repository_name: str
        :param observation_id: The observation identifier/content_id.
        :type observation_id: int
        :rtype: str
        """
        r = requests.get('/'.join([self.base_url, self.PATH,
                                   repository_name,
                                   str(observation_id)]))
        return r.json()


class WlDocumentRestApiClient(object):
    """
    The client for the WL Document REST API.
    `Documentation <https://api.weblyzard.com/doc/ui/#!/Document_API>`_
    """
    API_VERSION = 1.0

    DOCUMENTS_ENDPOINT = 'documents'
    ANNOTATE_ENDPOINT = 'annotate'

    def __init__(self, base_url):
        """
        Sets the base url for the API endpoint.

        :param base_url: The base URL without version number.
        :type base_url: str
        """
        self.base_url = '/'.join([base_url, str(self.API_VERSION)])

    def add_document(self, portal_name, document):
        """
        Adds the document to the given portal.

        :param portal_name: The portal to add the document to.
        :type portal_name: str
        :param document: The document to add. Either as JSON document \
                or as dict corresponding to the JSON format.
        :type document: str or dict
        :returns: The content_id of the added document.
        :rtype: int
        """
        if isinstance(document, dict):
            document = json.dumps(document)
        r = requests.post('/'.join([self.base_url, self.DOCUMENTS_ENDPOINT, portal_name]),
                          data=document,
                          headers={'Content-Type': 'application/json'})
        return r.json()

    def retrieve_document(self, portal_name, content_id):
        """
        Retrieve the document with content_id from portal_name.

        :param portal_name: The repository/matview name to add the document to.
        :type portal_name: str
        :param content_id: The document identifier/content_id.
        :type content_id: int
        :rtype: str
        """
        r = requests.get(
            '/'.join([self.base_url, self.DOCUMENTS_ENDPOINT, portal_name, str(content_id)]))
        return r.json()

    def update_document(self, portal_name, content_id, document):
        """
        Adds the document to the specified repository/matview.

        :param portal_name: The portal name to add the document to.
        :type portal_name: str
        :param content_id: The document identifier/content_id.
        :type content_id: int
        :param document: The document to add, in the weblyzard API JSON \
            document format.
        :type document: str
        :returns: A JSON string containing information about the update action.
        :rtype: str
        """
        if isinstance(document, dict):
            document = json.dumps(document)
        r = requests.put('/'.join([self.base_url,
                                   self.DOCUMENTS_ENDPOINT,
                                   portal_name,
                                   str(content_id)]),
                         data=document,
                         headers={'Content-Type': 'application/json'})
        return r.json()

    def delete_document(self, portal_name, content_id):
        """
        Deletes the document with the specified identifier. If a version is \
            provided, only that version is deleted.

        :param portal_name: The repository/matview name to add the document to.
        :type portal_name: str
        :param content_id: The document identifier/content_id.
        :type content_id: int
        :returns: A JSON string containing information about the delete action.
        :rtype: str
        """
        r = requests.delete('/'.join([self.base_url,
                                      self.DOCUMENTS_ENDPOINT,
                                      portal_name,
                                      str(content_id)]))
        return r.json()

    def annotate_document(self, document, analyzer_steps):
        """
        Annotate the given document and return it augmented with the given
        annotations. If no annotation_types are provided, a set of default
        annotations will be added.

        :param document: The document to annotate, in the weblyzard API JSON \
            document format or dict corresponding to it.
        :type document: str or 
        :param analyzer_steps: The types of annotation to add as a list of \
            strings.
        :type analyzer_steps: list
        :returns: The JSON document with added annotations.
        :rtype: str
        """
        assert isinstance(analyzer_steps, list)
        if isinstance(document, dict):
            document = json.dumps(document)
        r = requests.post('/'.join([self.base_url,
                                    self.ANNOTATE_ENDPOINT,
                                    '+'.join(analyzer_steps)]),
                          data=document,
                          headers={'Content-Type': 'application/json'})
        return(r.json())

    def check_document(self, document):
        """
        Checks the document's format.

        :param document: The document to annotate, in the weblyzard API JSON \
            document format or dict corresponding to it.
        :type document: str or 
        :returns: The result of the check.
        :rtype: str
        """
        if isinstance(document, dict):
            document = json.dumps(document)
        r = requests.post('/'.join([self.base_url,
                                    'check']),
                          data=document,
                          headers={'Content-Type': 'application/json'})
        return r.json()

    def get_status(self):
        """
        Calls the server's status method.
        """
        r = requests.get(self.base_url + '/status')
        return r.json()
