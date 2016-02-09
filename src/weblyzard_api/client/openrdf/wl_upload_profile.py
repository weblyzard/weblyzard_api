'''
Created on 14.02.2014

@author: heinz-peterlang
'''
import os

from weblyzard_api.client.openrdf import OpenRdfClient

def cleanup_config(service_url, config_repository):
    ''' '''
    client = OpenRdfClient(server_uri=service_url, 
                           config_repository=config_repository)
    client.cleanup_config()
    
def remove_profile(profile_name, config_repository, service_url):
    ''' '''
    client = OpenRdfClient(server_uri=service_url, 
                           config_repository=config_repository)
    client.remove_profile(profile_name)
    
def upload_profile(profile_fn, openrdf_server, config_repository, service_url=None):
    ''' '''
    client = OpenRdfClient(server_uri=openrdf_server, 
                           config_repository=config_repository)

    profile_name = profile_fn.split(os.sep)[-1].replace('.ttl', '')
    profile_definition = open(profile_fn).read()
    client.update_profile(profile_name, profile_definition)

if __name__ == '__main__':
    from argparse import ArgumentParser
    
    parser = ArgumentParser()
    parser.add_argument('--profile-file', dest='profile_fn', 
                        help='location of the profile definition file --> ttl')
    parser.add_argument('--remove-profile', dest='remove', 
                        help='location of the profile definition to remove')
    parser.add_argument('--clean', dest='clean', action='store_true', 
                        help='clean flag to clean weblyzard configuration repository')
    parser.add_argument('--service-url', dest='service_url', required=True, 
                        help='the service url to upload the profile to')
 
    args = parser.parse_args()

    if args.profile_fn:
        upload_profile(args.profile_fn, args.service_url)
    
    elif args.remove:
        remove_profile(args.remove, args.service_url)
        
    if args.clean:
        cleanup_config(args.service_url)

    print 'done :)'

    