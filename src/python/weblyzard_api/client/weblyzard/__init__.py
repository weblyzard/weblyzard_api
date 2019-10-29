#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Oct 29, 2019

.. codeauthor:: Max Göbel <goebel@weblyzard.com>
"""
import requests


class WlAuthenticatedApi(object):

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