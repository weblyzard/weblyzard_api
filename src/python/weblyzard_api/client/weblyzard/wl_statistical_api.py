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

logger = logging.getLogger('weblyzard_api.client.wl_statistical_api_client')


class WlStatisticalApiClient(WlAuthenticatedApi):
    """
    The client for the WL Statistics REST API.
    `Documentation <https://api.weblyzard.com/doc/ui/#!/Statistical_Data_API>`_

    """
    API_VERSION = 2.0

    PATH = 'observations'

    def __init__(self, base_url, username, password):
        """
        Sets the base url for the API endpoint.

        :param base_url: The base URL without version number.
        :type base_url: str
        """
        WlAuthenticatedApi.__init__(self, base_url, username, password)
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

    def get_status(self):
        """
        Calls the server's status method.
        """
        r = requests.get(self.base_url + '/status')
        return r.json()
