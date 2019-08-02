#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on Oct 24, 2016

@author: stefan
'''
from __future__ import unicode_literals

from past.builtins import basestring
from builtins import object
import json
import requests
import logging

logger = logging.getLogger(__name__)


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
        uri = kwargs['key']
        if uri.startswith('wl:'):
            lang, kw = uri.split(':')[1].split('/')
            uri = 'skbkw{}:{}'.format(lang, kw.replace(' ', '_'))
        elif uri.startswith('http://weblyzard.com/skb/keyword/'):
            lang = uri[len('http://weblyzard.com/skb/keyword/'):].split('/')[0]
        else:
            lang = None
        preferredName = kwargs.get(
            'preferred_name', kwargs.get('preferredName', None))
        skb_relevant_data = {'uri': uri,
                             'preferredName': '{}@{}'.format(preferredName, lang) if lang else preferredName,
                             'entityType': kwargs.get('entity_type', kwargs.get('entityType', None)),
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

    def save_entity(self, entity_dict, force_update=False):
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
        urlpath = self.ENTITY_PATH
        if force_update:
            urlpath = u'{}?force_update'.format(urlpath)
        response = requests.post('{}/{}'.format(self.url,
                                                urlpath),
                                 data=json.dumps(entity_dict),
                                 headers={'Content-Type': 'application/json'})
        if response.status_code < 400:
            return json.loads(response.text)['uri']
        else:
            return None

    def save_entity_batch(self, entity_list, force_update=False):
        '''
        Save a list of entities to the SKB, the individual entities encoded as 
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
        if len(entity_list) < 1:
            return None
        urlpath = self.ENTITY_BATCH_PATH
        if force_update:
            urlpath = u'{}?force_update'.format(urlpath)
        response = requests.post('{}/{}'.format(self.url,
                                                urlpath),
                                 data=json.dumps(entity_list),
                                 headers={'Content-Type': 'application/json'})
        if response.status_code < 400:
            return json.loads(response.text)['success']
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

    def check_entity_exists_in_skb(self, entity, entity_type):
        '''
        Check if a given entity already exists in the SKB. Supports both
        direct (i.e. URI as key) and `owl:sameAs` lookups.
        :param entity
        :param entity_type
        :returns: bool
        '''
        return self.check_existing_entity_key(entity, entity_type) is not None

    def check_existing_entity_key(self, entity, entity_type):
        '''
        If a given entity already exists in the SKB, as identified directly
        (i. e. by URI) or by `owl:sameAs` lookups, return the identifier of
        the existing equivalent entity
        :param entity
        :param entity_type
        :returns: uri of exisiting equivalent entity or None
        '''
        uri = entity.get('uri', entity.get('key', None))

        same_as = entity.get('owl:sameAs', [])
        if isinstance(same_as, basestring):
            same_as = [same_as]
        for uri in [uri] + same_as:
            try:
                if uri:
                    exact_match = self.get_entity(uri=uri)
                    if exact_match is not None:
                        return exact_match['uri']
                sameas_match = self.get_entity_by_property(
                    property_value=uri,
                    property_name='owl:sameAs',
                    entity_type=entity_type
                )
                if sameas_match is not None:
                    logger.info(
                        u'Identified entity {} through sameAs match.'.format(uri))
                    return sameas_match[0]['uri']
            except Exception as e:
                logger.error('Check if entity exists in SKB failed for %s: %s',
                             uri,
                             e)
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
