#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on Oct 24, 2016

@author: stefan
'''

import json
import requests


class SKBRESTClient(object):

    VERSION = 1.0
    TRANSLATION_PATH = '{}/skb/translation?'.format(VERSION)
    TITLE_TRANSLATION_PATH = '{}/skb/title_translation?'.format(VERSION)
    ENTITY_PATH = '{}/skb/entity'.format(VERSION)
    ENTITY_BATCH_PATH = '{}/skb/entity_batch'.format(VERSION)
    ENTITY_BY_PROPERTY_PATH = '{}/skb/entity_by_property'.format(VERSION)

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

    def clean_keyword_data(self, kwargs):
        """
        Prepare the keyword entity for SKB submission.
        :param kwargs
        """
        lang, kw = kwargs['key'].split(':')[1].split('/')
        uri = 'skbkw{}:{}'.format(lang, kw.replace(' ', '_'))
        skb_relevant_data = {'uri': uri,
                             'preferredName': kwargs['preferredName'],
                             'entityType': kwargs['entityType'],
                             'provenance': kwargs['provenance']}
        return skb_relevant_data

    def clean_recognize_data(self, kwargs):
        '''
        Helper class that takes the data generated from recognyze and keeps
        only the properties, preferred Name,  entityType, uri and profileName
        as provenance, if set.

        :param kwargs: The keyword data.
        :type kwargs: dict
        :returns: THe cleaned data.
        :rtype: dict
        '''
        skb_relevant_data = kwargs.get('properties', {})
        for key in ('entityType', 'preferredName'):
            if key in kwargs:
                skb_relevant_data[key] = kwargs[key]
        skb_relevant_data['uri'] = kwargs['key']
        if 'profileName' in kwargs:
            skb_relevant_data['provenance'] = kwargs['profileName']
        return skb_relevant_data

    def save_doc_kw_skb(self, kwargs):
        '''
        Saves the data for a keyword to the SKB, cleaning it first
        from document-specific information.

        :param kwargs: The entity data
        :type kwargs: dict
        :returns: The entity's uri.
        :rtype: str or unicode
        '''
        skb_relevant_data = self.clean_keyword_data(kwargs)
        return self.save_entity(entity_dict=skb_relevant_data)

    def save_entity(self, entity_dict):
        '''
        Save an entity to the SKB, the Entity encoded as `dict`.
        The `entity_dict` must contain a 'uri' and an 'entityType' entry.
        Adding a 'provenance' entry is encouraged, this should contain an
        identifier how the entity's information got obtained (e.g. profiles,
        query/script etc. used.

        Only exception (at the moment) is AgentEntity, where the SKB compiles
        the URI.

        :param entity_dict: The entity as dict
        :type entity_dict: `dict`
        :returns: The entity's uri or None, if an error occurred.
        :rtype: str or unicode or None.

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
        assert 'entityType' in entity_dict
        response = requests.post('{}/{}'.format(self.url,
                                                self.ENTITY_PATH),
                                 data=json.dumps(entity_dict),
                                 headers={'Content-Type': 'application/json'})
        if response.status_code < 400:
            return json.loads(response.text)['uri']
        else:
            return None

    def save_entity_batch(self, entity_list):
        '''
        Save a list of entities to the SKB, the individual Entities encoded as 
        `dict`.
        Each `entity_dict` must contain a 'uri' and an 'entityType' entry.
        Adding a 'provenance' entry is encouraged, this should contain an
        identifier how the entity's information got obtained (e.g. profiles,
        query/script etc. used.

        Only exception (at the moment) is AgentEntity, where the SKB compiles
        the URI.

        :param entity_list: The entities as list of dicts
        :type entity_dict: `list`
        :returns: The entities' uris or None, if an error occurred.
        :rtype: `list`
        '''
        for entity in entity_list:
            assert 'entityType' in entity
        response = requests.post('{}/{}'.format(self.url,
                                                self.ENTITY_BATCH_PATH),
                                 data=json.dumps(entity_list),
                                 headers={'Content-Type': 'application/json'})
        if response.status_code < 400:
            return json.loads(response.text)['uris']
        else:
            return None

    def get_entity_by_property(self, property_value, property_name=None, entity_type=None):
        '''
        Get an entity by a property's value. I.e. one can search for a twitter username
        and get a list of entities and their properties as result. Optionally, one can filter
        by entity_type and property_name (which then has to have `value`).

        It returns a list of dicts containing the properties of the matching entities or None
        if no entities matched.

        :param property_value: The property's value
        :type property_value: str or unicode
        :param property_name: The property's name. Optional.
        :type property_name: str or unicode
        :param entity_type: The type of entity to accept. Optional.
        :type entity_type: str or unicode
        :returns: The data of the entities matching the filter criteria.
        :rtype: list

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
                                params=params,
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

        :param uri: The uri of the Entity to get.
        :type uri: str or unicode
        :returns: The Entity's data.
        :rtype: dict

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
                                params=params,
                                headers={'Content-Type': 'application/json'})
        if response.status_code < 400:
            return json.loads(response.text)
        else:
            return None


class SKBSentimentDictionary(dict):
    SENTIMENT_PATH = '{}/skb/sentiment_dict'.format(SKBRESTClient.VERSION)

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
