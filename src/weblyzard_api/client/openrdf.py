#!/usr/bin/python
# -*- coding: utf8 -*-
'''
Created on 19.12.2013

@author: heinz-peterlang

For details: `check Sesame REST API<http://openrdf.callimachus.net/sesame/2.7/docs/system.docbook?view#The_Sesame_REST_HTTP_Protocol>`_

'''
import json
import requests
from pprint import pprint
from collections import namedtuple

RepositoryDetail = namedtuple('RepositoryDetail', ['id', 'uri', 'title'])

class OpenRdfClient(object):
    
    DEFAULT_HEADERS = {'Accept': 'application/sparql-results+json'}
    URL_MAPPING = {'get_repositories': ('/repositories', 'GET'),
                   'fetch_statements_repository': ('', 'GET')}
    
    def __init__(self, server_uri):
        ''' initializes the client
        :param server_uri: URL of the server
        '''
        self.server_uri = '%s/openrdf-sesame' % server_uri
        
    def request(self, function, data=None):
        ''' executes the requests to the TripleStores
        :param function: function (path) to request
        :param data: data to add to the POST request
        :returns: result of the server
        :rtype: json encoded dict
        '''
        print '%s/%s' % (self.server_uri, function)
        
        if data: 
            method = 'POST'
            headers = {'content-type': 'application/rdf+json'}
        else: 
            method = 'GET'
            headers = {'Accept': 'application/sparql-results+json'}
            
        r = requests.request(method, 
                             '%s/%s' % (self.server_uri, function), 
                             data=data, 
                             headers=headers)
        print r.text
        return json.loads(r.text) if r.text else r.text

    def get_repo_size(self, repo_id):
        
        result = self.request('repositories/%s/size' % repo_id)
        print 'get_repo_size', result
        
    def get_repositories(self):
        ''' '''
        
        result = self.request('repositories')
        repositories = {}
        
        if 'results' in result and 'bindings' in result['results']: 
            for repo in result['results']['bindings']:
                repo_id = repo['id']['value']
                repositories[repo_id]= RepositoryDetail(repo_id,
                                                        repo['uri']['value'],
                                                        repo['title']['value'])
                
        return repositories
    
    def repository_exists(self, repository_name):
        return repository_name in self.get_repositories()
    
    def get_all_statements(self, repository_name):
        result = self.request('repositories/%s/statements' % repository_name)
        pprint(result)
        
if __name__ == '__main__':
    
    client = OpenRdfClient('http://voyager.srv.weblyzard.net:8080')
    pprint(client.get_repositories())
    
    print client.repository_exists('test')
    print client.repository_exists('config.weblyzard.com')
    client.get_all_statements('SYSTEM')
#    client.get_repo_size('geonames')
    