'''
Created on Oct 24, 2016

@author: stefan
'''

import requests

class SKBRESTClient():
    
    PATH = '1.0/skb/translation?'

    def __init__(self, url, usr=None, pwd=None):
        '''
        :param url: URL of the jeremia web service
        :param usr: optional user name
        :param pwd: optional password
        '''
        self.url = url
    def translate(self, client_name, text, source_language, target_language):
#         url = ('http://localhost:5002/'
        url = ('%s/%s'
               'client=%s&'
               'term=%s&'
               'source=%s&'
               'target=%s' % (client_name, text, source_language, target_language))
        response = requests.get(url)
        print('response.text:', response.text)
        return(response.text, target_language)
        