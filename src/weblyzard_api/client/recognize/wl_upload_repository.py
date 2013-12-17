#!/usr/bin/python
# -*- coding: utf8 -*-
'''
Created on 17.12.2013

@author: heinz-peterlang

Before uploading a new repository, visit the web-interface and create the 
repository (type: Java Native store). 

ATTENTION: uploading the same dataset multiple times will lead to redundant data.

'''

import urllib
import httplib2
import os

from weblyzard_api.client import WEBLYZARD_API_URL

DEFAULT_HEADERS = {'content-type': 'application/x-turtle;charset=UTF-8'}

class UploadRecognizeRepository(object):

    def __init__(self, repository, graph_name, repo_base_url=WEBLYZARD_API_URL):

        if not repo_base_url.endswith('/'):
            repo_base_url = '%s/' % repo_base_url

        self.end_point_url = ''.join([repo_base_url, 
                                      'openrdf-sesame/repositories/',
                                      repository,
                                      '/statements?',
                                      urllib.urlencode({'context': '<%s>' % graph_name})])
    
    def run(self, src_directory):
        for fn in self.get_files(src_directory):
            self.upload_file(self.end_point_url, fn)
        
    @classmethod
    def upload_file(cls, end_point_url, fn, headers=DEFAULT_HEADERS):
        ''' uploads the file to the repository ''' 
        with open(fn, 'r') as f: 
            response, msg = httplib2.Http().request(end_point_url, 
                                                    'POST', 
                                                    body=f.read(), 
                                                    headers=headers)

            print "Response %s: %s" % (response.status, msg)

    @classmethod
    def get_files(cls, src_directory):
        for root, dirs, files in os.walk(src_directory):
            for fn in files: 
                if fn.endswith('.nt'):
                    yield os.path.join(src_directory, fn)

if __name__ == '__main__':
    from argparse import ArgumentParser
    
    parser = ArgumentParser(description='Uploads triples to an existing '
                            'Sesame repository. The script will not create '
                            'the repository, therefore create the repository '
                            'in the web-interface (type: java native type)')
    parser.add_argument('--source-dir', dest='source_directory', required=True, 
                        help='source directory containing nt files')
    parser.add_argument('--repo-base-url', dest='repo_base_url', 
                        default=WEBLYZARD_API_URL,
                        help='url of the tomcat server')
    parser.add_argument('--repository', required=True, 
                        help='name of the target repository')
    parser.add_argument('--graph-name', dest='graph_name', required=True,
                        help='name of the graph, e.g. http://dbpedia.org or'
                        ' http://geonames.org')
    
    args = parser.parse_args()
    
    upload = UploadRecognizeRepository(repository=args.repository, 
                                       graph_name=args.graph_name, 
                                       repo_base_url=args.repo_base_url)
    upload.run(src_directory=args.source_directory)