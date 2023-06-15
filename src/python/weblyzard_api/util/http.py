#!/usr/bin/python
# -*- coding: utf-8 -*-
#     @package weblyzard_api.utils.http
#     provides access to resources using http

# (C)opyrights 2008-2015 by Albert Weichselbraun <albert@weblyzard.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from future import standard_library
from typing import Dict
standard_library.install_aliases()

import time
import io
import urllib.request

from gzip import GzipFile
from random import randint
from urllib.parse import urlsplit, urlunsplit

# logging
import logging
log = logging.getLogger(__name__)

USER_AGENT = 'eWRT Version/0.1; Module %s +http://p.semanticlab.net/eWRT'
DEFAULT_WEB_REQUEST_SLEEP_TIME = 1
PROXY_SERVER = ''

RETRY_WAIT_TIME_RANGE = (2, 10)  # in seconds
# error codes which might trigger a retry:
HTTP_TEMPORARY_ERROR_CODES = (500, 503, 504)

# set default socket timeout (otherwise urllib might hang!)
from socket import setdefaulttimeout
DEFAULT_TIMEOUT = 60


def getHostName(x): return "://".join(urlsplit(x)[:2])


class Retrieve(object):
    """ @class Retrieve
        retrieves URLs using HTTP

        .. remarks:
           this class supports transparent
           - authentication and
           - compression
           - support for the context protocol (python)
           - automatic throttling support

        @warning
        There are certain urls such as
        http://www.mfsa.com.mt/insguide/english/glossarysearch.jsp?letter=all
        which are _not_ handled correctly by the underlying urllib2 library(!)
        Please use urllib in such cases.

    """

    __slots__ = ('module', 'sleep_time', 'last_access_time', 'user_agent',
                 '_supported_http_authentification_methods')

    def __init__(self, module, sleep_time=DEFAULT_WEB_REQUEST_SLEEP_TIME,
                 user_agent=USER_AGENT, default_timeout=DEFAULT_TIMEOUT):
        setdefaulttimeout(default_timeout)
        self.module = module
        self.sleep_time = sleep_time
        self.last_access_time = 0

        self._supported_http_authentification_methods = {
            'basic': Retrieve._getHTTPBasicAuthOpener,
            'digest': Retrieve._getHTTPDigestAuthOpener}

        self.user_agent = user_agent % self.module \
            if "%s" in user_agent else user_agent

    def open(self, url: str, user: str=None, pwd: str=None,
             data=None, headers: Dict={}, retry: int=0,
             authentification_method: str="basic", accept_gzip: bool=True,
             head_only: bool=False):
        """ Open a URL and returns the matching file object
            :param url: the URL to open
            :param user: optional user name
            :param pwd: optional password
            :param data: optional data to submit
            :param headers: a dictionary of optional headers
            :param retry: number of retries in case of an temporary error
            :param authentification_method: the used authentification_method
                        ('basic'*, 'digest')
            :param accept_gzip: flag to change the accepted encoding, gzip
                        or not
            :param head_only: if True: only execute a HEAD request
            :returns a file object for reading the url
        """
        auth_handler = self._supported_http_authentification_methods[
            authentification_method]
        urlObj = None
        tries = 0
        if isinstance(data, str):
            data = data.encode('utf-8')
        while not urlObj:
            request = urllib.request.Request(url, data, headers)

            if head_only:
                request.get_method = lambda: 'HEAD'

            request.add_header('User-Agent', self.user_agent)

            if accept_gzip:
                request.add_header('Accept-encoding', 'gzip')

            self._throttle()

            opener = []
            if PROXY_SERVER:
                opener.append(urllib.request.ProxyHandler({"http": PROXY_SERVER}))
            if user and pwd:
                opener.append(auth_handler(url, user, pwd))

            urllib.request.install_opener(urllib.request.build_opener(*opener))
            try:
                urlObj = urllib.request.urlopen(request)
            except urllib.error.HTTPError as e:
                if e.code in HTTP_TEMPORARY_ERROR_CODES and tries < retry:
                    sleep_time = randint(*RETRY_WAIT_TIME_RANGE)
                    log.info(f'retrying in {sleep_time}; received {e.code}')
                    time.sleep(sleep_time)
                    tries += 1
                    continue
                else:
                    raise e

            # check whether the data stream is compressed
            if urlObj.headers.get('Content-Encoding') == 'gzip':
                return self._getUncompressedStream(urlObj)

        return urlObj

    @staticmethod
    def _getHTTPBasicAuthOpener(url: str, user: str, pwd: str):
        """ Return an opener, capable of handling http-auth.
        :param url:
        :param user:
        :param pwd:
        """
        passman = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        passman.add_password(None, [url], user, pwd)
        auth_handler = urllib.request.HTTPBasicAuthHandler(passman)
        return auth_handler

    @staticmethod
    def _getHTTPDigestAuthOpener(url: str, user: str, pwd: str):
        """ Return an HTTP opener, capable of handling http-digest authentification.
        :param url:
        :param user:
        :param pwd:
        """
        passwdmngr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        passwdmngr.add_password('realm', url, user, pwd)
        auth_handler = urllib.request.HTTPDigestAuthHandler(passwdmngr)
        return auth_handler

    @staticmethod
    def _getUncompressedStream(urlObj):
        """ Transparently uncompress a given data stream.
        :param urlObj:
        :returns: an urlObj containing the uncompressed data
        """
        compressedStream = io.BytesIO(urlObj.read())
        return GzipFile(fileobj=compressedStream)

    def _throttle(self):
        """ delays web access according to the content provider's policy """

        if (time.time() - self.last_access_time) < \
                DEFAULT_WEB_REQUEST_SLEEP_TIME:
            time.sleep(self.sleep_time)
        self.last_access_time = time.time()

    def __enter__(self):
        """ support of the context protocol """
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """ context protocol support """
        if exc_type is not None:
            log.critical("%s" % exc_type)

    @staticmethod
    def get_user_password(url: str):
        """ Extract username and password from a URL, if present.
        :param url: well formed url, starting with a schema
        :return: tuple (new_url, user, password) """
        if not url.startswith('http'):
            url = 'http://%s' % url

        split_url = urlsplit(url)
        user = split_url.username
        password = split_url.password
        if user and password:
            new_url = (split_url.scheme,
                       split_url.netloc.replace('%s:%s@' % (user, password),
                                                ''),
                       split_url.path,
                       split_url.query,
                       split_url.fragment)
            url = urlunsplit(new_url)
        else:
            assert not user and not password, 'if set, user AND pwd required'

        return url, user, password

    @staticmethod
    def add_user_password(url: str, user: str, password: str):
        split_url = urlsplit(url)
        return urlunsplit((split_url.scheme,
                           '%s:%s@%s' % (user, password, split_url.netloc),
                           split_url.path,
                           split_url.query,
                           split_url.fragment))
