#!/usr/bin/python
# -*- coding: utf8 -*-
'''
Created on 19.12.2013

@author: heinz-peterlang

For details: `check Sesame REST API<http://openrdf.callimachus.net/sesame/2.7/docs/system.docbook?view#The_Sesame_REST_HTTP_Protocol>`_

http://www.csee.umbc.edu/courses/graduate/691/spring14/01/examples/sesame/openrdf-sesame-2.6.10/docs/system/ch08.html

'''
import ast
import urllib
import httplib2
import os
import json
import requests
import unittest

from pprint import pprint
from collections import namedtuple
from urllib import urlencode
from SPARQLWrapper import SPARQLWrapper, JSON


QUERIES = {
           'configured_profiles': '''
                PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>
                PREFIX re: <http://www.semanticlab.net/prj/recognize/voc/>
                SELECT ?s ?profile_name ?analyzer
                WHERE {
                       ?s rdfs:label  ?profile_name .
                       ?s re:analyzer ?analyzer .
                }''',
        'all_subjects': '''
            select distinct ?s where {?s ?p ?o}
        '''
}

RepositoryDetail = namedtuple('RepositoryDetail', ['id', 'uri', 'title'])

class OpenRdfClient(object):

    DEFAULT_HEADERS = {'Accept': 'application/sparql-results+json'}
    URL_MAPPING = {'get_repositories': ('/repositories', 'GET'),
                   'fetch_statements_repository': ('', 'GET')}

    def __init__(self, server_uri, config_repository='config.weblyzard.com'):
        ''' initializes the client
        :param server_uri: URL of the server
        '''
        if not 'openrdf-sesame' in server_uri:
            server_uri = '%s/openrdf-sesame' % server_uri

        self.server_uri = server_uri
        self.repository_url_tmplt = self.server_uri + '/repositories/%s'
        self.config_repository = config_repository

    def run_query(self, repository_name, query):
        sparql = SPARQLWrapper(self.repository_url_tmplt % repository_name)
        sparql.setQuery(query.strip())
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        for result in results['results']['bindings']:
            yield result


    def cleanup_config(self):
        ''' '''
        for orphan in self.get_orphaned_analyzers():
            self.delete_statements(self.config_repository,
                                           subj='_:%s'%orphan,
                                           delete=True)

    def get_orphaned_analyzers(self):
        profiles = self.get_profiles()
        configured = []
        for profile in profiles.itervalues():
            configured.extend(profile['analyzers'])

        orphaned = []
        query = QUERIES['all_subjects']
        for result in self.run_query(self.config_repository, query):
            name = result['s']['value']
            if name.startswith('genid'):
                if name in configured:
                    pass
                else:
                    orphaned.append(name)
        return orphaned

    def get_profiles(self):
        ''' returns a dictionary (subject_uri, profile_name) for all profiles
        configured in the config repositoriy
        '''
        self.check_config_repo()

        query = QUERIES['configured_profiles']
        profiles = {}

        for result in self.run_query(self.config_repository, query):
            profile = {}
            profile_name = result['profile_name']['value']
            profile['subject_uri'] = result['s']['value']
            profile['analyzers'] = [result['analyzer']['value']]
            if profile_name in profiles:
                profiles[profile_name]['analyzers'].extend(profile['analyzers'])
            else:
                profiles[profile_name] = profile

        return profiles

    def remove_profile(self, profile_name):
        ''' Removes a given profile name '''
        subject_uris = []
        profiles = self.get_profiles()
        if profile_name in profiles:
            profile = profiles[profile_name]
            if not profile_name.startswith('pr:'):
                profile_name = 'pr:%s' % profile_name

            subject_uris.extend(['<%s>'%analyzer for analyzer in profile['analyzers']])
            subject_uris.append('<%s>'%profile['subject_uri'])

        if len(subject_uris):
#             if not subject_uri.startswith('pr:'):
#                 subject_uri = 'pr:%s' % subject_uri
#             if not subject_uri.endswith('>'):
#                 subject_uri = '%s>' % subject_uri
            for subject_uri in subject_uris:
                try:
                    self.delete_statements(self.config_repository,
                                           subj=subject_uri,
                                           delete=True)
                except Exception, e:
                    print e

    def update_profile(self, profile_name, profile_definition):
        ''' Updates the given profile on the server '''

        profiles = self.get_profiles()

        if profile_name in profiles:
            print profile_name
            subject_uri = profiles[profile_name]

            # TODO: check why we need to fix this????
            if not subject_uri.endswith('>'):
                subject_uri = '%s>' % subject_uri

            self.delete_statements(self.config_repository,
                                   subj=subject_uri,
                                   delete=True)
        self.upload_statement(content=profile_definition,
                              context='config.weblyzard.com',
                              target_repository=self.config_repository)

    def check_config_repo(self):
        repositories = self.get_repositories()

        if not self.config_repository in repositories:
            print 'warning config repo "%s" does not exist' % self.config_repository

    def request(self, function, data=None, params=None, delete=False,
                content_type='applicatoni/rdf+json',
                accept='application/sparql-results+json'):
        ''' executes the requests to the TripleStores
        :param function: function (path) to request
        :param data: data to add to the POST request
        :returns: result of the server
        :rtype: json encoded dict
        '''
        print '%s/%s' % (self.server_uri, function)

        if data:
            method = 'POST'
            headers = {'content-type': content_type}
        else:
            if delete:
                method = 'DELETE'
            else:
                method = 'GET'
            headers = {'Accept': accept}

            if params:
                function = '%s?%s' % (function, params)

        print method, '%s/%s' % (self.server_uri, function)

        r = requests.request(method,
                             '%s/%s' % (self.server_uri, function),
                             data=data,
                             headers=headers)
        text = r.text

        if isinstance(text, unicode):
            text = text.encode('utf-8')

        try:
            return json.loads(r.text) if r.text else r.text
        except Exception, e:
            print text
            return text
        
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

    def delete_statements(self, repository_name, subj=None, pred=None, obj=None,
                          delete=False):
        function = 'repositories/%s/statements' % repository_name

        params = {}
        if subj: params['subj'] = subj
        if pred: params['pred'] = pred
        if obj: params['obj'] = obj
        if params:
            params = '&'.join(['%s=%s' % (k, v) for k, v in params.iteritems()])
        else:
            params = None

        return self.request(function, params=params, delete=delete)

    def upload_statement(self, content, context, target_repository):

        params = 'context=%s' % context
        function = 'repositories/%s/statements' % target_repository

        self.request(function, content, params, delete=False,
                     content_type='application/x-turtle;charset=UTF-8')

    def execute_query(self, query, repository):
        params = { 'query': query }
        headers = {
          'content-type': 'application/x-www-form-urlencoded',
          'accept': 'application/sparql-results+json'
        }
        endpoint = "%s/%s/statements" % (self.server_uri, repository)
        (response, content) = httplib2.Http().request(endpoint, 'POST', 
                                                      urllib.urlencode(params),
                                                      headers=headers)
        return (response,ast.literal_eval(content))
      
    def execute_update(self, query, repository, server_url):
        params = { 'update': query }
        headers = {
          'content-type': 'application/x-www-form-urlencoded',
          'accept': 'application/sparql-results+json'
        }
        repository_url = self.repository_url_tmplt % repository
        endpoint = "%s/statements" % (repository_url)
        (response, content) = httplib2.Http().request(endpoint, 'POST', 
                                                      urllib.urlencode(params),
                                                      headers=headers)
        response = response['status']
        return(response)
      
    def delete_triples_by_types(self, repository, types):
        
        for rdf_type in types:
            query = 'DELETE ?s WHERE {?s ?p ?o FILTER(?s = <%s>)}' % rdf_type
            self.execute_update(query, repository)
            
    def upload_repo_from_file(self, filename, repository):
        base_fn = os.path.basename(filename)
        
        assert base_fn.endswith('ttl')
        
        graph  = 'file://%s'%base_fn
        params = { 'context': '<' + graph + '>' }
        endpoint = "%s/%s/statements?%s" % (self.server_uri, repository, 
                                            urllib.urlencode(params))
        
        print("Loading %s into %s in Sesame" % (filename, endpoint))
        
        data = open(filename, 'r').read()
        (response, content) = httplib2.Http().request(endpoint, 'PUT', 
                                                      body=data, 
                                                      headers={'content-type': 'application/x-turtle'})
        print("Response %s" % response.status)
        print(content)
    
if __name__ == '__main__':
    unittest.main()
