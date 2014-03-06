#!/usr/bin/python
# -*- coding: utf8 -*-
'''
Created on 17.12.2013

@author: heinz-peterlang

Before uploading a new repository, visit the web-interface and create the 
repository (type: Java Native store). 

ATTENTION: uploading the same dataset multiple times will lead to redundant data.

'''
import os

from weblyzard_api.client import WEBLYZARD_API_URL

# DEFAULT_HEADERS = {'content-type': }

from weblyzard_api.client.openrdf import OpenRdfClient

def get_files(src_directory, file_ext='.nt'):
    for root, dirs, files in os.walk(src_directory):
        for fn in files: 
            if fn.endswith(file_ext):
                yield os.path.join(src_directory, fn)

def upload_directory(src_directory, repository, graph_name, 
                     server_url=WEBLYZARD_API_URL, file_ext='.nt'):
    ''' uploads all files with the correct file extension to the repository '''

    client = OpenRdfClient(server_url)

    for fn in get_files(src_directory=src_directory, file_ext=file_ext):
        client.upload(open(fn).read(), graph_name, repository)

if __name__ == '__main__':
    from argparse import ArgumentParser
    
    parser = ArgumentParser(description='Uploads triples to an existing '
                            'Sesame repository. The script will not create '
                            'the repository, therefore create the repository '
                            'in the web-interface (type: java native type)')
    parser.add_argument('--source-dir', dest='source_directory', required=True, 
                        help='source directory containing nt files')
    parser.add_argument('--server-url', dest='server_url', 
                        default=WEBLYZARD_API_URL,
                        help='url of the tomcat server')
    parser.add_argument('--repository', required=True, 
                        help='name of the target repository')
    parser.add_argument('--graph-name', dest='graph_name', required=True,
                        help='name of the graph, e.g. http://dbpedia.org or'
                        ' http://geonames.org')
    
    args = parser.parse_args()
    upload_directory(server_url=args.server_url, 
                     src_directory=args.src_directory, 
                     repository=args.repository, 
                     graph_name=args.graph_name)
