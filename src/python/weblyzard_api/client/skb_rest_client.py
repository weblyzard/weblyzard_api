#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on Oct 24, 2016

@author: stefan
'''

from builtins import object
import json
import logging
from typing import List, Optional

import requests
from weblyzard_api.client.rdf import prefix_uri

logger = logging.getLogger(__name__)


class SKBRESTClient(object):

    VERSION = 1.0
    TRANSLATION_PATH = '{}/skb/translation?'.format(VERSION)
    TITLE_TRANSLATION_PATH = '{}/skb/title_translation?'.format(VERSION)
    ENTITY_PATH = '{}/skb/entity'.format(VERSION)
    ENTITY_BATCH_PATH = '{}/skb/entity_batch'.format(VERSION)
    ENTITY_URI_BATCH_PATH = '{}/skb/entity_uri_batch'.format(VERSION)
    ENTITY_SEARCH_PATH = '{}/skb/entity/search'.format(VERSION)
    ENTITY_LOOKUP_PATH = '{}/skb/entity/lookup'.format(VERSION)

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

    def clean_keyword_data(self, kwargs) -> Optional[dict]:
        """
        Prepare the keyword entity for SKB submission.
        :param kwargs
        """
        uri = kwargs.get('key')
        if not uri:
            return None

        lang, gen_pos = None, None

        if uri.startswith('http://weblyzard.com/skb/keyword/'):
            prefix = 'http://weblyzard.com/skb/keyword/'

            prefix_stripped_uri = uri[len(prefix):]
            uri_elements = prefix_stripped_uri.split('/')

            # extract lang and general POS if possible
            if len(uri_elements) == 2:
                lang, _ = uri_elements
                if len(lang) != 2:  # likely not a lang
                    lang = None
            elif len(uri_elements) == 3:
                lang, gen_pos, _ = uri_elements

        preferred_name = kwargs.get('preferred_name', kwargs.get('preferredName'))
        entity_type = kwargs.get('entity_type', kwargs.get('entityType'))

        skb_relevant_data = {'uri': uri,
                             'preferredName': f'{preferred_name}@{lang}'if lang else preferred_name,
                             'entityType': entity_type,
                             'provenance': kwargs['provenance']}
        if gen_pos:
            skb_relevant_data['lexinfo:partOfSpeech'] = gen_pos
        return skb_relevant_data

    def clean_recognize_data(self, kwargs):
        # TODO: This might not be needed anymore.
        '''
        Helper fn that takes the data generated from recognyze and keeps
        only the properties, preferred Name, entityType, uri and profileName
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

    def save_doc_kw_skb(self, kwargs) -> dict:
        '''
        Saves the data for a keyword to the SKB, cleaning it first
        from document-specific information.
        '''
        skb_relevant_data = self.clean_keyword_data(kwargs)
        return self.save_entity(entity_dict=skb_relevant_data)

    def save_entity(self, entity_dict:dict, force_update:bool=False,
                    ignore_cache:bool=False) -> Optional[dict]:
        '''
        Save an entity to the SKB, the Entity encoded as `dict`.
        The `entity_dict` must contain a 'uri' and an 'entityType' entry
        and the 'provenance', i.e. an identifier how the entity's information 
        got obtained (e.g. repository, profiles, query/script etc. used).

        If no URI is sent the SKB attempts to compile a weblyzard-namespaced custom
        entity URI from the preferredName or a name rdf predicate (this needs to exist).

        :param entity_dict: the entity as dict
        :param force_update: force a comparison and update on any existing SKB values
        :param ignore_cache: bypass recently requested URI cache
        :returns: json response as dict or None, if an error occurred

        >>> response = skb_client.save_entity({
            "entityType": "OrganizationEntity",
            "provenance": "custom_entity_20210101",
            "rdfs:label": "Hello world!",
            "thumbnail": "https://s0.wp.com/i/blank.jpg",
            "twitter": "@HelloWorld",
        })
        >>> print(response) = {
            "data": {
                    "entityType": "OrganizationEntity",
                    "uri": "http://weblyzard.com/skb/entity/organization/hello_world",
                    "preferredName": "Hello world!"
                    "preferredNameByLang": "Hello world!"
                    "rdfs:label": "Hello world!",
                    "wdt:P18": "https://s0.wp.com/i/blank.jpg",
                    "twitter username": "@HelloWorld",
            },
            "uri": "http://weblyzard.com/skb/entity/organization/hello_world",
            "message": "success",
            "info": "added entity",
            "reason": null,
            "status": 200
        }
        '''
        assert 'entityType' in entity_dict
        assert 'provenance' in entity_dict

        params = {'force_update': force_update,
                  'ignore_cache': ignore_cache}

        response = requests.post(url=f'{self.url}/{self.ENTITY_PATH}',
                                 params=params,
                                 json=entity_dict,
                                 )
        return self.drop_error_responses(response)

    def drop_error_responses(self, response):
        if response.status_code < 400:
            return json.loads(response.text)
        else:
            logger.error(f'request failed {response.text}')
            return None

    def save_entity_uri_batch(self, uri_list:List[str], language:str,
                              force_update:bool=False,
                              ignore_cache:bool=False,
                              headers:dict=None) -> Optional[dict]:
        '''
        Send a batch of shortened entity URIs to the SKB for storage.
        :param uri_list: list of shorted URIs of one of those forms
                1.'{entity_type abbr}:{repository abbr}:{id}'
                with entity_type abbr: P, G, O, E and short repository: wd, osm, gn
                2. '{entity_type}:{entity uri}
                e.g. 'RocheEntity:http://ontology.roche.com/ROX1305279964642'
        :param header: request header
        :param language: language filter for preferredName result
        :param force_update: update existing SKB values via Jairo
        :param ignore_cache: bypass recently requested URI cache
        :returns: json response as dict or None, if an error occurred
        '''

        if len(uri_list) < 1:
            return None

        params = {'force_update': force_update,
                  'ignore_cache': ignore_cache,
                  'language': language}

        response = requests.post(url=f'{self.url}/{self.ENTITY_URI_BATCH_PATH}',
                                 params=params,
                                 headers=headers,
                                 json=uri_list,
                                 )
        return self.drop_error_responses(response)

    def save_entity_batch(self, entity_list:List[dict], force_update:bool=False,
                          ignore_cache:bool=False, headers:dict=None) -> Optional[dict]:
        '''
        Save a list of entities to the SKB, the individual entities encoded as 
        `dict`. Each `entity_dict` must contain an 'entityType' and a 
        'provenance' entry, which is an identifier how the entity's information 
        got obtained (e.g. repository, profiles, query/script etc. used).

        If no URI is sent the SKB attempts to compile a weblyzard-namespaced custom
        entity URI from the preferredName or a name rdf predicate (this needs to exist).
        
        :param entity_list: entities as list of dicts
        :param force_update: force a comparison and update on any existing SKB values
        :param ignore_cache: bypass recently requested URI cache
        :returns: json response as dict or None, if an error occurred
        
        
        >>> skb_client.save_entity_batch(entity_list=[
            {'entityType': 'PersonEntity', 'provenance': 'unittest', 
            'rdfs:label': 'PersonTest', 'occupation':'wd:Q82955'},
            {'entityType': 'GeoEntity', 'provenance': 'unittest', 
            'gn:name': 'GeoTest', 'gn:alternateName': 'GeographyEntity', 'gn:countryCode':'AT'},
            {'entityType': 'OrganizationEntity', 'provenance': 'unittest', 
            'gn:name': 'OrgTest', 'rdfs:label': ['OrgTest@en', 'OT@de'], 'wdt:P17':'wd:Q40'},
        ])
        >>> print(response) = {
            'success': {'http://weblyzard.com/skb/entity/person/persontest': 'PersonTest', 
                        'http://weblyzard.com/skb/entity/geo/geotest': 'GeoTest', 
                        'http://weblyzard.com/skb/entity/organization/orgtest': 'OrgTest'}, 
            'error': {}, 
            'summary': {'success': 3, 
                        'loaded': 0, 
                        'added': 3, 
                        'updated': 0, 
                        'error': 0, 
                        'total': 3
                        }
        }
        '''

        if len(entity_list) < 1:
            return None

        for entity_dict in entity_list:
            assert 'entityType' in entity_dict
            assert 'provenance' in entity_dict

        params = {'force_update': force_update,
                  'ignore_cache': ignore_cache}

        response = requests.post(url=f'{self.url}/{self.ENTITY_BATCH_PATH}',
                                 params=params,
                                 headers=headers,
                                 json=entity_list,
                                 )
        return self.drop_error_responses(response)

    def get_entity_by_property(self, property_value:str, property_name:str=None,
                               entity_type:str=None, exact_match:bool=False) -> Optional[List[dict]]:
        '''
        Get an entity by a property's value.
        Returns a list of dicts containing the properties of the matching entities or None
        if no entities matched.
        
        .. caveat: universal access rights, i.e. ALL entities are returned
        
        :param property_value: the property's value
        :param property_name: the property's name, either LOD predicate or 
            human-readable form (optional)
        :param entity_type: type of the entity (optional)
        :param exact_match: if True only exact matches for the property value are returned
        '''

        if property_name:
            if exact_match:
                filters = [{'filter_type': 'property',
                            'filter_values': {'name': property_name,
                                              'value': property_value,
                                              'operator':'term'}}]
            else:
                filters = [{'filter_type': 'property',
                            'filter_values': {'name': property_name,
                                              'value': property_value}}]
            return self.entity_search(entity_type=entity_type,
                                      filters=filters)
        else:
            return self.entity_search(search_phrase=property_value,
                                      entity_type=entity_type)

    def get_entity_by_tag(self, tag_value:str, tag_prefix:str=None,
                          entity_name:str=None, entity_type:str=None,
                          should_fallback:bool=True) -> Optional[dict]:
        '''
        Get an entity by a `tag`.
        :param tag_value: the value of the tag
        :param tag_prefix: the tag prefix indicating what the value represents
        :param entity_name: (optional) entity preferredName or other name
        :param entity_type: (optional) entity type
        :param should_fallback: if False only return exact `entity_name` matches,
            else return the best matching results
            
        .. note: tags that include a `tag_prefix` are NOT found if only the
                `tag_value` is provided
        '''

        if tag_prefix:
            tag = f'{tag_prefix}:{tag_value}'
        else:
            tag = tag_value

        filters = [{'filter_type': 'keywordfield',
                    'filter_values': {'field': 'tags',
                                      'filter_conditions': {'must': tag}}}]

        if entity_name:
            # exact name search
            result = self.entity_search(search_phrase=f'"{entity_name}"',
                                        search_field='title',
                                        entity_type=entity_type,
                                        filters=filters)
            if not result and should_fallback:
                logger.info(f"returning best matching results for" +
                            f"entity {entity_name} with tag {tag}")
                result = self.entity_search(search_phrase=f'{entity_name}',
                                            search_field='title',
                                            entity_type=entity_type,
                                            filters=filters)
        else:
            result = self.entity_search(entity_type=entity_type,
                                        filters=filters)

        return result

    def entity_search(self, search_phrase:str=None, search_field:str=None, entity_type=None,
                      fuzzy=False, search_languages:List[str]=None, response_language:str=None,
                      access_right='universal', filters:List[dict]=None) -> Optional[List[dict]]:
        '''
        Search for entities with a search phrase that is matched on property values
        with additional search filters. Search type is text `match` (analyzed, full-text).
        :param search_phrase: (optional) string to search for
        :param search_field: `all` - all properties (default), 
                             `uri` - entity uri, 
                             `title` - preferredName and name fields, 
                             `description` - description and abstracts, 
                             `title/description` - title and description properties
        :param entity_type: (optional) the type of entity
        :param fuzzy: enable fuzzy search
        :param search_languages: (optional) only search in properties that match the given
            list of languages, `None` is a valid value for properties with no specified language  
        :param response_language: (optional) names and descriptions are returned only in that language
        :param access_right: if not set only returns openly accessibly entities
            (default `universal` returns all entities) 
        :param filters: additional entity filters specified by `filter_type` and `filter_values`, 
                valid filters are:
                `PropertyFilter` -`filter_type`: `property`
                    `filter_values`: `name`, `value`, `operator` (optional), `negate` (optional)
                `DateFilter` - `filter_type`: `anniversary`
                    `filter_values`: `start_date` (optional), `end_date` (optional)
                `AnniversaryFilter` - `filter_type`: `date`
                    `filter_values`: either `day` (mm-dd)  or `from_date`, `end_date`, 
                                    `anniv_num` (optional)       
        '''
        params = {'response_format': 'simple', 'human_readable':False}
        if search_phrase:
            params['search_phrase'] = search_phrase
        if search_field:
            params['search_field'] = search_field
        if entity_type:
            params['entity_type'] = entity_type
        if fuzzy:
            params['fuzzy_search'] = fuzzy
        if search_languages:
            params['search_languages'] = search_languages
        if response_language:
            params['response_language'] = response_language
        if access_right:
            params['access_right'] = access_right

        if filters:
            payload = {'filters': filters}
        else:
            payload = {}

        response = requests.post(f'{self.url}/{self.ENTITY_SEARCH_PATH}',
                                params=params,
                                json=payload)
        return self.drop_error_responses(response)

    def get_entity(self, uri:str) -> Optional[dict]:
        '''
        Get an entity by its uri.
        Returns a dict containing the properties of the entity or None
        if no entities matched.

        :param uri: uri of the entity
        '''

        params = {'uri': uri}
        response = requests.get(f'{self.url}/{self.ENTITY_PATH}',
                                params=params,
                                headers={'Content-Type': 'application/json'})
        return self.drop_error_responses(response)

    def entity_uri_lookup(self, entity_uris:List[str]) -> dict:
        '''
        Very fast lookup of entity uris, only checks the _id field.
        :param entity_uris: list of uris
        '''
        response = requests.post(f'{self.url}/{self.ENTITY_LOOKUP_PATH}',
                                 json=entity_uris,
                                 headers={'Content-Type': 'application/json'})
        return self.drop_error_responses(response)

    def check_entity_exists_in_skb(self, entity:dict, entity_type:str) -> bool:
        '''
        Check if a given entity already exists in the SKB. Supports both
        direct (i.e. URI as key) and `owl:sameAs` lookups.
        :param entity: entity dict containing `uri` or `owl:sameAs`
        :param entity_type: the entity type
        
        .. caveat: universal access rights
        '''
        return self.check_existing_entity_key(entity, entity_type) is not None

    def check_existing_entity_key(self, entity:dict, entity_type:str) -> Optional[str]:
        '''
        If a given entity already exists in the SKB, as identified directly
        (i. e. by URI) or by `owl:sameAs` lookups, return the identifier of
        the existing equivalent entity. 
        
        .. caveats: only returns the first entry if multiple are found,
            universal access rights
            
        :param entity: entity dict containing `uri`/`key` or `owl:sameAs`
        :param entity_type: the entity type
        '''
        uri = entity.get('uri', entity.get('key'))
        same_as = entity.get('owl:sameAs', [])

        if isinstance(same_as, str):
            same_as = [same_as]

        if uri:
            exact_match = self.get_entity(uri=uri)
            if exact_match is not None:
                return exact_match['uri']

        for uri in same_as:
            sameas_matches = None
            sameas_matches = self.get_entity_by_property(property_value=prefix_uri(uri),
                                                         property_name='owl:sameAs',
                                                         entity_type=entity_type,
                                                         exact_match=True)
            if not sameas_matches:
                sameas_matches = self.get_entity_by_property(property_value=uri,
                                                         property_name='owl:sameAs',
                                                         entity_type=entity_type,
                                                         exact_match=True)
            if sameas_matches:
                logger.info(f'Identified entity {uri} through sameAs match.')
                if len(sameas_matches) > 1:
                    logger.info(f'More than one matching entity ({len(sameas_matches)}) for {uri} found.')
                return sameas_matches[0]['uri']

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


class SKBSimpleBaseFormsDictionary(dict):
    BASE_FORMS_PATH = '{}/skb/baseforms'.format(SKBRESTClient.VERSION)

    def __init__(self, url):
        self.url = '{}/{}'.format(url, self.BASE_FORMS_PATH)
        res = requests.get(self.url)
        if res.status_code < 400:
            response = json.loads(res.text)
            data = self.reconstruct(response)
            dict.__init__(self, data)

    def reconstruct(self, response):
        return_value = {}
        for k, v in response.items():
            return_value[k] = self.reconstruct(v) if isinstance(v, dict) else (set(v) if isinstance(v, list) else v)
        return return_value
