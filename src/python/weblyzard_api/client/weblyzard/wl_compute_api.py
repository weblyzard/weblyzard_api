#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Oct 29, 2019

.. codeauthor:: Max Göbel <goebel@weblyzard.com>
"""
import json
import requests
import logging

logger = logging.getLogger('weblyzard_api.client.wl_compute_rest_api_client')


class WlComputeApiClient(object):
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

    def check_active(self):
        """ Check if the Compute API is up an healthy.
        """
        try:
            r = requests.get(
                '/'.join([self.base_url, self.ENDPOINT_STATUS])).status_code
            return r.status_code == 200
        except Exception as e:
            logger.warn(e)
        return False

