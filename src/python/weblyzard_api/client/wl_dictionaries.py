#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 20.01.2014

@author: heinz-peterlang

The source files for the dictionaries (of format *.csv and *.txt) are being
copied by Jenkins from the opinion-mining-lexicon repository to 
services.weblyzard.com.
'''
import os
import urlparse
from datetime import datetime, timedelta
from socket import gethostbyname, gaierror
from urlparse import urlsplit
from warnings import warn
    
from eWRT.access.http import Retrieve

LOCAL_DIR = '/opt/weblyzard/dictionaries/'
SERVER_URL = 'https://services.weblyzard.com/repo/resources/'
MAX_AGE_HOURS = 24

class WeblyzardDictionaries(object):
        
    def __init__(self, user, password, 
                 local_dir=LOCAL_DIR, 
                 server_url=SERVER_URL, 
                 max_age_hours=MAX_AGE_HOURS):
        
        if not os.path.exists(local_dir):
            os.makedirs(local_dir)
        self.max_file_age = datetime.now() - timedelta(hours=max_age_hours)
        self.local_dir = local_dir 
        self.server_url = server_url
        self.retrieve = Retrieve(__file__)
        self.user = user
        self.password = password

    @staticmethod
    def is_online(server_url):
        '''
        Checks, whether the given url is online.

        :param server_url: \
            the url to check.

        :returns:
            True, if the dictionary server is online/reachable.
        '''
        hostname = urlparse.urlsplit(server_url).netloc
        try:
            gethostbyname(hostname)
            return True
        except gaierror:
            return False

        
    def get_dictionary(self, dictionary_uri):
        ''' tries to load the dictionary from the file-system. If the function
        cannot find the file or if the file is too old (see MAX_AGE_HOURS), 
        the function will load the dictionary from the server.
        :param dictionary_uri: URI for the dictionary, e.g. people/de/titles/all.txt
        :returns: full file name of the dictionary
        '''
        
        if dictionary_uri.startswith('/'):
            dictionary_uri = dictionary_uri[1:]
        
        full_path = os.path.join(self.local_dir, dictionary_uri)

        # skip retrieval, if the server is not available
        if not self.is_online(SERVER_URL):
            return full_path

        fetch_file = True

        if os.path.isfile(full_path):
            last_mod = datetime.fromtimestamp(os.path.getmtime(full_path))
        
            if last_mod < self.max_file_age:
                last_mod_server = self.get_last_mod_date(dictionary_uri)
                
                if last_mod_server < last_mod: 
                    fetch_file = False
            else: 
                fetch_file = False
                
        if fetch_file: 
            self.get_from_server(dictionary_uri, full_path)
            
        return full_path

    def get_last_mod_date(self, dictionary_uri):
        ''' Requests the URL with a HEAD request to retrieve the last_modified 
        date of the file
        :param dictionary_uri: URI for the dictionary, e.g. people/de/titles/all.txt
        ''' 
        
        full_url = urlparse.urljoin(self.server_url, dictionary_uri)
        response = self.retrieve.open(full_url, 
                                      user=self.user, 
                                      pwd=self.password,
                                      accept_gzip=False,
                                      head_only=True)
        last_modified = response.headers.get('Last-Modified')
        
        if last_modified:
            return datetime.strptime(last_modified, '%a, %d %b %Y %H:%M:%S %Z')
        
    def get_from_server(self, dictionary_uri, target_path):
        ''' Fetches a dictionary from the server and stores it on the local FS.
        :param dictionary_uri: URI for the dictionary, e.g. people/de/titles/all.txt
        :param target_path: destination on local FS to store the file
        :returns: target_path if the file was saved
        '''
        
        full_url = urlparse.urljoin(self.server_url, dictionary_uri)
        response = self.retrieve.open(full_url, 
                                      user=self.user, 
                                      pwd=self.password)
        
        if response:
            target_directory =  os.path.dirname(target_path)
            
            if not os.path.exists(target_directory):
                    os.makedirs(target_directory)
                
            with open(target_path, 'w') as f: 
                f.write(response.read())
                
            return target_path
    
    

def test_is_online():
    url = "http://not-existinet-url-123.de/myservice"
    assert WeblyzardDictionaries.is_online(url) == False

