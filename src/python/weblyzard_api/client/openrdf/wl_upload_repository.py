#!/usr/bin/python
# -*- coding: utf8 -*-
'''
Created on 17.12.2013
@author: heinz-peterlang
Before uploading a new repository, visit the web-interface and create the
repository (type: Java Native store).
ATTENTION: uploading the same dataset multiple times will lead to redundant data.
'''
import os.path

from weblyzard_api.client import WEBLYZARD_API_URL

# DEFAULT_HEADERS = {'content-type': }

from weblyzard_api.client.openrdf import OpenRdfClient

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i+n]
        
def get_files(src_directory, file_ext=None):
    file_list = []
    for _, _, files in os.walk(src_directory):
        for fn in files:
            if file_ext and fn.endswith(file_ext):
                file_list.append(os.path.join(src_directory, fn))
            else:
                file_list.append(os.path.join(src_directory, fn))

    file_list.sort(key=lambda f: os.path.splitext(f))
    return file_list

def upload_directory(src_directory, repository=None, graph_name=None,
                     server_url=WEBLYZARD_API_URL, file_ext=None, 
                     chunk_size=100000, max_retry=5):
    ''' uploads all files with the correct file extension to the repository '''

    client = OpenRdfClient(server_url)
    available_repositories = client.get_repositories()
    print 'Reading directory %s' % src_directory
    for fname in get_files(src_directory=src_directory, file_ext=file_ext):
        extension = os.path.splitext(fname)[-1]

        if not extension.lower() in ['.ttl', '.nt']:
            print 'Skipping file: %s' % fname
            continue

        print 'Processing file: %s' % fname

        if not repository and not graph_name:
#             if extension=='.ttl':
#                 #extract repository and graph name from file
#                 with open(fname) as f:
#                     for line in f.readlines():
#                         if line.startswith('pr:'):
#                             repository = line.split(':')[-1]
#                             graph_name = repository.split('.')[0]
#                             break                     
            repository = fname.split('/')[-1]
            repository = repository.replace(extension, '')
            graph_name = repository.split('.')[0]

        if repository in available_repositories:
            print 'uploading %s to repository %s' % (fname, repository)
            lines = open(fname).readlines()
            for chunk in chunks(lines, chunk_size):
                success = False
                retry = 0
                while not success and retry<max_retry:
                    try:
                        chunk = '\n'.join(chunk)
                        client.upload(chunk, graph_name, repository)
                        success = True
                    except Exception, e:
                        print e
                        retry += 1
                        
                if not success:
                    print('Could not upload chunk, skipping...')
        else:
            print '%s does not exist on machine %s, please add...' % (repository,
                                                                      server_url)

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
    parser.add_argument('--repository', help='name of the target repository')
    parser.add_argument('--graph-name', dest='graph_name',
                        help='name of the graph, e.g. http://dbpedia.org or'
                        ' http://geonames.org')
    parser.add_argument('--chunk-size', dest='chunk_size', type=int, default=100000)
    parser.add_argument('--num-retries', dest='retries', type=int, default=5)

    args = parser.parse_args()
    upload_directory(server_url=args.server_url,
                     src_directory=args.source_directory,
                     repository=args.repository,
                     graph_name=args.graph_name,
                     chunk_size=args.chunk_size,
                     max_retry=args.retries)
