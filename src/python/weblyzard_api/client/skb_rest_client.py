#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on Oct 24, 2016

@author: stefan
'''

import json
import requests


class SKBRESTClient(object):

    TRANSLATION_PATH = '1.0/skb/translation?'
    TITLE_TRANSLATION_PATH = '1.0/skb/title_translation?'
    KEYWORD_PATH = '1.0/skb/keyword_annotation'
    ENTITY_PATH = '1.0/skb/entity'
    ENTITY_BY_PROPERTY_PATH = '1.0/skb/entity_by_property'

    def __init__(self, url):
        '''
        :param url: URL of the SKB web service
        '''
        self.url = url

    def translate(self, **kwargs):
        response = requests.get(
            '%s/%s' % (self.url, self.TRANSLATION_PATH), params=kwargs)
        if response.status_code < 400:
            return(response.text, kwargs['target'])
        else:
            return None

    def title_translate(self, **kwargs):
        response = requests.get(
            '%s/%s' % (self.url, self.TITLE_TRANSLATION_PATH), params=kwargs)
        if response.status_code < 400:
            return(response.text, kwargs['target'])
        else:
            return None

    def save_doc_kw_skb(self, kwargs):
        response = requests.post('%s/%s' % (self.url, self.KEYWORD_PATH),
                                 data=json.dumps(kwargs),
                                 headers={'Content-Type': 'application/json'})
        if response.status_code < 400:
            return response.text
        else:
            return None

    def save_entity(self, entity_dict):
        '''
        >>> uri = skb_client.save_entity({
            "publisher": "You Don't Say",
            "title": "Hello, world!",
            "url": "http://www.youdontsayaac.com/hello-world-2/",
            "charset": "UTF-8",
            "thumbnail": "https://s0.wp.com/i/blank.jpg",
            "locale": "en_US",
            "last_modified": "2014-07-15T18:46:42+00:00",
            "page_type": "article",
            "published_date": "2014-07-15T18:46:42+00:00",
            "twitter_site": "@mfm_Kay",
            "twitter_card": "summary"
        })
        >>> print(uri)
        http://weblyzard.com/skb/entity/agent/you_don_t_say
        '''
        response = requests.post('{}/{}'.format(self.url,
                                                self.ENTITY_PATH),
                                 data = json.dumps(entity_dict),
                                 headers={'Content-Type': 'application/json'})
        if response.status_code < 400:
            return json.loads(response.text)['uri']
        else:
            return None

    def get_entity_by_property(self, property_value, property_name=None, entity_type=None):
        '''
        Get an entity by a property's value. I.e. one can search for a twitter username
        and get a list of entities and their properties as result. Optionally, one can filter
        by entity_type and property_name (which then has to have `value`).

        It returns a list of dicts containing the properties of the matching entities or None
        if no entities matched.

        >>> skb_client.get_entity_by_property(property_value="You Don't Say")
        [{u'entityType': u'AgentEntity', u'uri': u'http://weblyzard.com/skb/entity/agent/you_don_t_say', u'last_modified': u'2018-05-17T13:16:24.779019', u'_id': u'agent:you_don_t_say', u'properties': {u'url': u'youdontsayaac.com', u'publisher': u"You Don't Say", u'locale': u'en_US', u'twitter_site': u'@mfm_Kay', u'thumbnail': u'https://s0.wp.com/i/blank.jpg'}, u'preferredName': u"You Don't Say"}]
        '''
        params = {'value': property_value}
        if property_name:
            params['property_name'] = property_name
        if entity_type:
            params['entity_type'] = entity_type
        response = requests.get('{}/{}'.format(self.url,
                                               self.ENTITY_BY_PROPERTY_PATH),
                                params = params,
                                headers={'Content-Type': 'application/json'})
        if response.status_code < 400:
            return json.loads(response.text)
        else:
            return None

    def get_entity(self, uri):
        '''
        Get an entity by its uri.

        It returns a dict containing the properties of the entity or None
        if no entities matched.

        >>> skb_client.get_entity(uri="http://weblyzard.com/skb/entity/agent/you_don_t_say")
        {u'publisher': u"You Don't Say", u'locale': u'en_US', u'entityType': u'AgentEntity', u'thumbnail': u'https://s0.wp.com/i/blank.jpg', u'url': u'youdontsayaac.com', u'twitter_site': u'@mfm_Kay', u'preferredName': u"You Don't Say"}
        '''
        if 'http://weblyzard.com/skb/entity/' in uri:
            uri = uri.replace('http://weblyzard.com/skb/entity/', '')
            prefix = uri.split('/')[0]
            uri = '{}:{}'.format(prefix, '/'.join(uri.split('/')[1:]))
        params = {'uri': uri}
        response = requests.get('{}/{}'.format(self.url,
                                               self.ENTITY_PATH),
                                params = params,
                                headers={'Content-Type': 'application/json'})
        if response.status_code < 400:
            return json.loads(response.text)
        else:
            return None


class SKBSentimentDictionary(dict):
    SENTIMENT_PATH = '1.0/skb/sentiment_dict'

    def __init__(self, url, language, emotion='polarity'):
        self.url = '{}/{}'.format(url,
                                  self.SENTIMENT_PATH)
        res = requests.get(self.url,
                           params={'lang': language,
                                   'emotion': emotion})
        if res.status_code < 400:
            response = json.loads(res.text)
            data = {}
            for document in response:
                data[(document['term'], document['pos'])] = document['value']
            dict.__init__(self, data)
        else:
            dict.__init__(self, {})
