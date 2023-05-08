#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
**webLyzard web service clients**

.. codeauthor:: Albert Weichselbraun <albert.weichselbraun@htwchur.ch>
.. codeauthor:: Heinz-Peter Lang <lang@weblyzard.com>
migrated from `eWRT` 2021
"""
from __future__ import unicode_literals, print_function

from future import standard_library
standard_library.install_aliases()

from os import getenv
from typing import List, Dict

from builtins import range
from builtins import object
import traceback
import logging
import random
import json

from urllib.parse import urlencode
from six import string_types
from json import dumps, loads
from functools import partial
from socket import setdefaulttimeout

from weblyzard_api.util.http import Retrieve

# set higher timeout values
WS_DEFAULT_TIMEOUT = 900

WEBLYZARD_API_URL = getenv("WEBLYZARD_API_URL") or "http://localhost:8080"
WEBLYZARD_API_USER = getenv("WEBLYZARD_API_USER")
WEBLYZARD_API_PASS = getenv("WEBLYZARD_API_PASS")

OGER_API_URL = getenv("OGER_API_URL")

logger = logging.getLogger(__name__)


class RESTClient(object):
    """
    class:: RESTClient
    """

    def __init__(self, service_url: str, user: str=None, password: str=None,
                 authentification_method: str='basic',
                 module_name: str='eWRT.REST',
                 default_timeout: int=WS_DEFAULT_TIMEOUT):
        """ 
        :param service_url: the base url of the web service
        :param modul_name: the module name to add to the USER AGENT
                               description (optional)
        :param user: username
        :param password: password
        :param authentification_method: authentification method to use
                                        ('basic'*, 'digest').
        :param default_timeout: default request timeout
        """
        # remove superfluous slashes, if required
        self.service_url = service_url[:-1] if service_url.endswith("/") \
            else service_url
        self.user = user
        self.password = password

        if not default_timeout:
            default_timeout = WS_DEFAULT_TIMEOUT

        url_obj = Retrieve(module_name, sleep_time=0,
                           default_timeout=default_timeout)
        self.retrieve = partial(url_obj.open,
                                user=user,
                                pwd=password,
                                authentification_method=authentification_method
                                )

    def _json_request(self, url: str, parameters: Dict=None,
                      parse_result: bool=True, return_plain: bool=False,
                      json_encode_arguments: bool=True,
                      content_type: str='application/json'):
        """ Execute a given JSON request.
        :param url: the url to query
        :param parameters: optional parameters
        :param parse_result: a flag to return message only
        :param return_plain: whether to return the result without prior
                             deserialization using json.load (False*)
        :param json_encode_arguments: whether to json encode the parameters
                                      (True*)
        :param content_type: one of 'application/json', 'application/xml'
        """
        if parameters:
            handle = self.retrieve(
                url,
                dumps(parameters) if json_encode_arguments else parameters,
                {'Content-Type': content_type})
        else:
            handle = self.retrieve(url)

        if parse_result:
            response = handle.read()
            if response:
                return response if return_plain else loads(response.decode('utf8'))
            else:
                # this will also return empty list, dicts ...
                return response
        return handle

    @staticmethod
    def get_request_url(service_url: str, command: str, identifier: str=None,
                        query_parameters: str=None):
        """ Return the request url given the command and query parameters.
        :param base_url: the base url of the web service
        :param command: the command to execute at the web service
        :param identifier: an optional identifier (e.g. batch_id, ...)
        :param query_parameters: query parameters to include in the url
                                 (e.g. execute?debug=True)
        :rtype: the complete request url
        """
        # remove superfluous slashes
        if command.startswith("/"):
            command = command[1:]

        url = '%s/%s/%s' % (service_url, command, identifier) \
            if identifier else "%s/%s" % (service_url, command)

        # add query string, if necessary
        if query_parameters:
            url = url + "?" + urlencode(query_parameters, doseq=True)

        return url

    def execute(self, command: str, identifier: str=None, parameters: Dict=None,
                parse_result: bool=True, return_plain: bool=False,
                json_encode_arguments: bool=True, query_parameters: str=None,
                content_type: str='application/json'):
        """ Execute a given JSON command on the given web service
        :param command: the command to execute
        :param identifier: an optional identifier (e.g. batch_id, ...)
        :param parameters: optional post parameters
        :param parse_result: a flag to return message only
        :param return_plain: return the result without prior deserialization
                             using json.load (False*)
        :param json_encode_arguments: whether to json encode the parameters
        :param query_parameters: optional query parameters
        :rtype: the query result
        """
        url = self.get_request_url(self.service_url, command, identifier,
                                   query_parameters)

        logger.debug(f'Requesting url {url}')

        return self._json_request(url=url, parameters=parameters,
                                  parse_result=parse_result,
                                  return_plain=return_plain,
                                  json_encode_arguments=json_encode_arguments,
                                  content_type=content_type)


class MultiRESTClient(object):
    """ Allow multiple URLs for access REST services """
    MAX_BATCH_SIZE = 500
    URL_PATH: str = ''

    def __init__(self, service_urls, user=None, password=None,
                 default_timeout=WS_DEFAULT_TIMEOUT, use_random_server=True):

        self._service_urls = self.fix_urls(service_urls, user, password)

        if use_random_server:
            random.shuffle(self._service_urls)

        self.clients = self._connect_clients(self._service_urls,
                                             default_timeout=default_timeout)

    def is_online(self):
        try:
            self.request('status')
            return True
        except:
            return False

    @classmethod
    def fix_urls(cls, urls: List[str],
                 user: str=None, password: str=None) -> List[str]:
        """ Fix URLs and put them into the correct format, to maintain
            the compability to the remaining platform.
        :param urls: service urls
        :type urls: string or list or tuple
        :param user: username
        :param password: password
        :returns: correctly formated urls
        :rtype: list
        """
        correct_urls = []

        if isinstance(urls, string_types):
            urls = [urls]

        for url in urls:
            if not url.endswith('/'):
                url = '%s/' % url

            if not '/rest' in url:
                if cls.URL_PATH and not url.endswith(cls.URL_PATH):
                    if cls.URL_PATH.startswith('/'):
                        cls.URL_PATH = cls.URL_PATH[1:]
                    url = '%s%s' % (url, cls.URL_PATH)

            if user and password:
                url = Retrieve.add_user_password(url, user, password)

            correct_urls.append(url)

        return correct_urls

    @classmethod
    def _connect_clients(cls, service_urls, user=None, password=None,
                         default_timeout=WS_DEFAULT_TIMEOUT):

        clients = {}

        for url in service_urls:
            if not isinstance(url, str):
                continue
            if url.startswith('{'):
                url = json.loads(url)
                count = len(url.keys())
            elif '<' in url:
                param = url[url.find("<") + 1:url.find(">")]
                if '%' in param:
                    _, count = param.split('%')
                    count = int(count)
                    for i in range(0, count):
                        url_i = url.replace(f'<{param}>', f'{i}')

                        if user is None and password is None:
                            url_i, user, password = Retrieve.get_user_password(url_i)

                        clients[i] = RESTClient(service_url=url_i,
                                                user=user,
                                                password=password,
                                                default_timeout=default_timeout)
                    return clients
            else:

                if user is None and password is None:
                    url, user, password = Retrieve.get_user_password(url)

                # append to end
                clients[len(clients)] = RESTClient(service_url=url,
                                                   user=user,
                                                   password=password,
                                                   default_timeout=default_timeout)
        return clients

    def request(self, path: str, parameters: Dict=None, source_id: int=None,
                parse_result: bool=True, return_plain: bool=False,
                json_encode_arguments: bool=True,
                query_parameters: str=None, content_type: str='application/json',
                execute_all_services: bool=False, pass_through_exceptions=()):
        """ Execute a given JSON request.
        :param path: the path to query
        :param parameters: optional parameters
        :param parse_result:
        :param source_id: optional source_id param
        :param pass_through_exceptions:
            set to True, if the client shall pass through all exceptions
        :param return_plain: whether to return the result without prior
                             deserialization using json.load (False*)
        """
        response = None
        errors = []

        clients = []
        if source_id is not None and source_id > 0:
            client_id = source_id % len(self.clients)
            if client_id in self.clients:
                clients = [self.clients[client_id]]

        if not len(clients):
            clients = self.clients.values()

        for client in clients:
            try:
                response = client.execute(
                    command=path,
                    parameters=parameters,
                    parse_result=parse_result,
                    return_plain=return_plain,
                    json_encode_arguments=json_encode_arguments,
                    query_parameters=query_parameters,
                    content_type=content_type)

                if not execute_all_services:
                    break

            except Exception as e:
                if pass_through_exceptions:
                    raise e
                else:
                    msg = 'Could not execute %s %s, error %s\n%s' % (
                        client.service_url, path, e,
                        traceback.format_exc())
                    logger.warning(msg, exc_info=True)
                    errors.append(msg)

        if len(errors) == len(self.clients):
            print ('\n'.join(errors))
            raise Exception('Could not make request to path %s: %s' % (
                path,
                '\n'.join(errors)))

        return response

    def get_service_urls(self):
        """ """
        return [client.service_url for client in self.clients.values()]

    @classmethod
    def get_document_batch(cls, documents, batch_size=None):
        batch_size = batch_size if batch_size else cls.MAX_BATCH_SIZE
        for i in range(0, len(documents), batch_size):
            yield documents[i:i + batch_size]

