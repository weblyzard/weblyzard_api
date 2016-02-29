'''
Created on 14.02.2014
@author: heinz-peterlang
'''
import os
import urlparse

from weblyzard_api.client.openrdf import OpenRdfClient

def cleanup_config(service_url, config_repository):
    ''' '''
    client = OpenRdfClient(server_uri=service_url,
                           config_repository=config_repository)
    client.cleanup_config()

def remove_profile(profile_name, service_url, config_repository):
    ''' '''
    client = OpenRdfClient(server_uri=service_url,
                           config_repository=config_repository)
    client.remove_profile(profile_name)

def upload_profile(profile_fn, service_url, config_repository):
    ''' '''


    client = OpenRdfClient(server_uri=service_url,
                           config_repository=config_repository)
    available_repositories = client.get_repositories()
    
    profile_fns = []
    if os.path.isdir(profile_fn):
        for root, dirs, files in os.walk(profile_fn):
            for fn in files:
                if fn.endswith('.ttl'):
                    profile_fns.append('%s/%s' % (root, fn))
    else:
        profile_fns = [profile_fn]

    print('Found %s profiles, uploading to %s' % (len(profile_fns), service_url))
    print profile_fns
    for p_fns in profile_fns:
        profile_name = p_fns.split(os.sep)[-1].replace('.ttl', '')
        profile_definition = open(p_fns).read()

        print('Processing profile %s' % profile_name)
        if service_url:
            url = urlparse.urlparse(service_url)
            hostname = '%s://%s' % (url.scheme, url.netloc)
            profile_definition = profile_definition.replace('$HOSTNAME', hostname)
            repo_name = [line for line in profile_definition.split('\n') if 'dcterms:source' in line][0]
            repo_name = repo_name.replace('";','').split('/')[-1].strip()
            if not repo_name in available_repositories:
                print('Skipping profile %s: bad repository' % profile_name)
                continue
            client.update_profile(profile_name, profile_definition)

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('--profile-file', dest='profile_fn',
                        help='location of the profile definition file --> ttl')
    parser.add_argument('--remove-profile', dest='remove',
                        help='location of the profile definition to remove')
    parser.add_argument('--config-repository', dest='config_repo',
                        help='location of the profile definitions')
    parser.add_argument('--clean', dest='clean', action='store_true',
                        help='clean flag to clean weblyzard configuration repository')
    parser.add_argument('--service-url', dest='service_url', required=True,
                        help='the service url to upload the profile to')

    args = parser.parse_args()

    if args.profile_fn:
        upload_profile(profile_fn=args.profile_fn,
                       service_url=args.service_url,
                       config_repository=args.config_repo)

    elif args.remove:
        remove_profile(profile_fn=args.profile_fn,
                       service_url=args.service_url,
                       config_repository=args.config_repo)

    if args.clean:
        cleanup_config(service_url=args.service_url,
                       config_repository=args.config_repo)

    print('done :)')
