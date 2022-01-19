#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import os
import unittest

import mock
import pytest
from weblyzard_api.client.skb_rest_client import SKBRESTClient


class MockResponse:

    def __init__(self, json_data, text, status_code):
        self.json_data = json_data
        self.text = text
        self.status_code = status_code

    def json(self):
        return self.json_data


class TestSKBRESTClientTranslations(unittest.TestCase):

    def setUp(self):
        url = 'http://skb-rest-translation.prod.i.weblyzard.net:8443'  # prod
        # url = 'http://localhost:5000'
        self.skb_client = SKBRESTClient(url)

    def test_translations_request(self):
        expected_translations = {'knall': 'bang', 'falle': 'trap', 'fall': 'case'}
        for source in expected_translations:
            result = self.skb_client.translate(term=source,
                                               source='de',
                                               target='en')
            assert(result[0] == expected_translations[source])
            assert(result[1] == 'en')

    @mock.patch('weblyzard_api.client.skb_rest_client.requests.get')
    def test_title_translations_request(self, mock_get):
        source = "Die schmerzhaften, aber sehr selten tödlichen Folgen eines" \
        "Witwenbisses gehen auf die besondere Struktur der Latrotoxine zurück"
        expected_translation = "The painful but very rarely fatal consequences" \
        "of a widow's bite are due to the special structure of the latrotoxins"

        mock_get.return_value = MockResponse(text=expected_translation,
                                             json_data=None,
                                             status_code=200)

        result = self.skb_client.title_translate(client='google',
                                                 text=source,
                                                 source='de',
                                                 target='en')
        assert(result[0] == expected_translation)
        assert(result[1] == 'en')


class TestSKBRESTClientEntities(unittest.TestCase):

    def setUp(self):
        url = 'http://skb-rest-entities.prod.i.weblyzard.net:8443'  # prod
        url = 'http://localhost:5000'
        self.skb_client = SKBRESTClient(url)

    def test_clean_keyword_data(self):
        kw_annotation = {
            "topEntityId": "energy",
            "confidence": 786.2216230656553,
            "entities": [{
                "surfaceForm": "energy",
                "start": 112,
                "end": 118,
                "sentence": 0
            }],
            "grounded": True,
            "scoreName": "CONFIDENCE x OCCURENCE",
            "entityType": "GemetEntity",
            "score": 786.22,
            "key": "http://www.eionet.europa.eu/gemet/concept/2712",
            "provenance": "en.gemet",
            "properties": {
                "definition": "The capacity to do work; involving thermal energy (heat), radiant energy (light), kinetic energy (motion) or chemical energy; measured in joules."
            },
            "preferredName": "energy"
        }
        cleaned = self.skb_client.clean_keyword_data(kw_annotation)
        assert cleaned == {
            "entityType": "GemetEntity",
            "uri": "http://www.eionet.europa.eu/gemet/concept/2712",
            "provenance": "en.gemet",
            "preferredName": "energy"
        }

        kw_annotation = {
            "confidence": 0.0,
            "grounded": True,
            "entityType": "NonEntityKeyword",
            "score": 0.0,
            "key": "http://weblyzard.com/skb/keyword/en/noun/equator",
            "provenance": "save_skb_entities",
            "preferredName": "equator"
        }
        cleaned = self.skb_client.clean_keyword_data(kw_annotation)
        assert cleaned == {
            "entityType": "NonEntityKeyword",
            "uri": "http://weblyzard.com/skb/keyword/en/noun/equator",
            "provenance": "save_skb_entities",
            "preferredName": "equator@en",
            "lexinfo:partOfSpeech": "noun"
        }

        # missing pos
        kw_annotation = {
            "entityType": "NonEntityKeyword",
            "key": "http://weblyzard.com/skb/keyword/fr/privé",
            "provenance": "save_skb_entities",
            "preferredName": "privé"
        }
        cleaned = self.skb_client.clean_keyword_data(kw_annotation)
        assert cleaned == {
            "entityType": "NonEntityKeyword",
            "uri": "http://weblyzard.com/skb/keyword/fr/privé",
            "provenance": "save_skb_entities",
            "preferredName": "privé@fr",
        }

        # missing lang
        kw_annotation = {
            "entityType": "NonEntityKeyword",
            "key": "http://weblyzard.com/skb/keyword/solo",
            "provenance": "save_skb_entities",
            "preferredName": "solo"
        }
        cleaned = self.skb_client.clean_keyword_data(kw_annotation)
        assert cleaned == {
            "entityType": "NonEntityKeyword",
            "uri": "http://weblyzard.com/skb/keyword/solo",
            "provenance": "save_skb_entities",
            "preferredName": "solo",
        }

    @mock.patch('weblyzard_api.client.skb_rest_client.requests.post')
    def test_save_keyword(self, mock_post):
        kw_annotation = {"entities": [
                            {
                              "confidence": 2955.790126821422,
                              "end": 137,
                              "sem_orient": 0.0,
                              "start": 129,
                              "surfaceForm": "raincoat"
                            }
                          ],
                          "entityType": "NonEntityKeyword",
                          "entity_metadata": {},
                          "key": "http://weblyzard.com/skb/keyword/en/noun/raincoat",
                          "preferredName": "raincoat",
                          "significance": 2955.790126821422
                        }
        kw_annotation['provenance'] = 'unittest'

        response = {"message": "success",
                    "info": "added entity",
                    "uri": "http://weblyzard.com/skb/keyword/en/noun/raincoat",
                    "data": {"lexinfo:partOfSpeech": "noun",
                             "preferredNameByLang": "raincoat@en",
                             "uri": "http://weblyzard.com/skb/keyword/en/noun/raincoat",
                             "entityType": "NonEntityKeyword",
                             "preferredName": "raincoat",
                             "tags": []
                            }
                    }
        mock_post.return_value = MockResponse(text=json.dumps(response),
                                              json_data={},
                                              status_code=201)
        assert(self.skb_client.save_doc_kw_skb(kw_annotation)['uri'] ==
               "http://weblyzard.com/skb/keyword/en/noun/raincoat")

    # # create new entity
    # response = client.save_entity(entity_dict={'entityType': 'PersonEntity', 'provenance': 'unittest', 'rdfs:label': 'TestPerson', 'uri':'http://my_test'})
    # print(response)
    # # update entity
    # response = client.save_entity(entity_dict={'entityType': 'PersonEntity', 'provenance': 'unittest', 'rdfs:label': 'UpdatedTestPerson', 'uri':'http://my_test'}, force_update=True)
    # print(response)
    # time.sleep(3)  # wait to make sure cache was updated
    # response = client.save_entity(entity_dict={'entityType': 'PersonEntity', 'provenance': 'unittest', 'rdfs:label': 'TestPerson', 'uri':'http://my_test'}, force_update=True)
    # print(response)
    # # explicitly ignore cache to update again
    # response = client.save_entity(entity_dict={'entityType': 'PersonEntity', 'provenance': 'unittest', 'rdfs:label': 'TestPerson', 'uri':'http://my_test'}, force_update=True, ignore_cache=True)
    # print(response)

    # response = client.save_entity_uri_batch(uri_list=['P:wd:Q76'], language='en', force_update=False, ignore_cache=False)
    # print(response)
    # response = client.save_entity_uri_batch(uri_list=['PersonEntity:http://www.wikidata.org/entity/Q23'], language='en', force_update=False, ignore_cache=False)
    # print(response)

    # response = client.save_entity_batch(entity_list=[{'entityType': 'PersonEntity', 'provenance': 'unittest', 'rdfs:label': 'PersonTest', 'occupation':'wd:Q82955'},
    #                                                  {'entityType': 'GeoEntity', 'provenance': 'unittest', 'gn:name': 'GeoTest', 'gn:alternateName': 'GeographyEntity', 'gn:countryCode':'AT'},
    #                                                  {'entityType': 'OrganizationEntity', 'provenance': 'unittest', 'gn:name': 'OrgTest', 'rdfs:label': ['OrgTest@en', 'OT@de'], 'wdt:P17':'wd:Q40'},
    #                                                  ])

    def test_get_entity_by_property(self):
        '''
        For this test the expected entities must be present in the SKB index.
        '''
        response = self.skb_client.get_entity_by_property(property_value='BarackObama',
                                                          property_name='twitter username',
                                                          exact_match=True)
        print([f"{entity['uri']}, {entity['preferredName']}" for entity in response])

        assert(len(response) == 1)
        entity = response[0]
        assert(entity['uri'] == 'http://www.wikidata.org/entity/Q76')
        assert(entity['preferredName'] == 'Barack Obama')
        assert(entity['wdt:P2002'] == 'BarackObama')

        response = self.skb_client.get_entity_by_property(property_value='BarackObama',
                                                          property_name='wdt:P2003')
        assert(len(response) == 1)
        entity = response[0]
        assert(entity['uri'] == 'http://www.wikidata.org/entity/Q76')
        assert(entity['preferredName'] == 'Barack Obama')
        assert(entity['wdt:P2003'] == 'barackobama')  # also matches on instagram user `brackobama`

        response = self.skb_client.get_entity_by_property(property_value='"Barack Obama"',
                                                          property_name='abstract',
                                                          entity_type='PersonEntity')
        assert(response)
        result = [(entity['uri'], entity['preferredName']) for entity in response]
        print('\n'.join([str(r) for r in result]))
        assert(set([('http://www.wikidata.org/entity/Q76', 'Barack Obama'),
                    ('http://www.wikidata.org/entity/Q13133', 'Michelle Obama'),
                    ('http://www.wikidata.org/entity/Q434706', 'Elizabeth Warren'),
                    ('http://www.wikidata.org/entity/Q6279', 'Joe Biden'),
                    ('http://www.wikidata.org/entity/Q235349', 'Jill Biden'),
                    ]).issubset(set(result)))

        response = self.skb_client.get_entity_by_property(property_value='Siemens',
                                                          property_name='preferredName',
                                                          entity_type='OrganizationEntity')
        assert(response)
        result = [(entity['uri'], entity['preferredName']) for entity in response]
        print('\n'.join([str(r) for r in result]))
        assert(set([('http://www.wikidata.org/entity/Q81230', 'Siemens'),
                    ('http://www.wikidata.org/entity/Q30338724', 'Siemens (Austria)'),
                    ('http://www.wikidata.org/entity/Q54969704', 'Siemens Healthcare'),
                    ]).issubset(set(result)))

    def test_get_entity(self):
        '''
        For this test the expected entities must be present in the SKB index.
        '''
        expected = {'http://www.wikidata.org/entity/Q76': 'http://www.wikidata.org/entity/Q76',
                    'wd:Q76': 'http://www.wikidata.org/entity/Q76',
                    'http://weblyzard.com/skb/entity/organization/weblyzard': None,
                    'skborg:weblyzard': None}
        for uri, exp in expected.items():
            result = self.skb_client.get_entity(uri)
            if exp:
                assert(result['uri'] == exp)
            else:
                assert(result == exp)

    def test_check_existing_entity(self):
        '''
        For this test the expected entities must be present in the SKB index.
        '''
        result = self.skb_client.check_existing_entity_key(
            entity={'uri': 'http://sws.geonames.org/2761367/'},
            entity_type='GeoEntity')
        assert(result == 'http://sws.geonames.org/2761367/')

        result = self.skb_client.check_entity_exists_in_skb(
            entity={'owl:sameAs': 'wd:Q1741'},
            entity_type='GeoEntity')
        assert(result == True)

    def test_get_entity_by_tag(self):
        '''
        For this test the expected entities must be present in the SKB index.
        '''
        result = self.skb_client.get_entity_by_tag(tag_value='journalist',
                                                     tag_prefix='occupation',
                                                     entity_name='Armin Wolf',
                                                     entity_type='PersonEntity',
                                                     should_fallback=False)
        assert(len(result) == 1)
        entity = result.pop()
        assert(entity['uri'] == 'http://www.wikidata.org/entity/Q688378')
        assert(entity['preferredName'] == 'Armin Wolf')

        result = self.skb_client.get_entity_by_tag(tag_value='occupation:journalist',
                                                     entity_name='Armin Wolf',
                                                     entity_type='PersonEntity',
                                                     should_fallback=False)

        assert(len(result) == 1)
        entity = result.pop()
        assert(entity['uri'] == 'http://www.wikidata.org/entity/Q688378')
        assert(entity['preferredName'] == 'Armin Wolf')

        result = self.skb_client.get_entity_by_tag(tag_value='geo:city',
                                                   entity_name='York',
                                                   entity_type='GeoEntity')

        result = [(entity['uri'], entity['preferredName']) for entity in result]
        print('\n'.join([str(r) for r in result]))
        assert(set([('http://sws.geonames.org/5128581/', 'New York'),
                    ('http://sws.geonames.org/2633352/', 'York'),
                    ]).issubset(set(result)))

    # def test_save_entity(self):
    #     entity_data = {
    #         u"publisher": u"You Don't Say",
    #         u"title": u"Hello, world!",
    #         u"url": u"http://www.youdontsayaac.com/hello-world-2/",
    #         u"charset": u"UTF-8",
    #         u"thumbnail": u"https://s0.wp.com/i/blank.jpg",
    #         u"locale": u"en_US",
    #         u"last_modified": u"2014-07-15T18:46:42+00:00",
    #         u"page_type": u"article",
    #         u"published_date": u"2014-07-15T18:46:42+00:00",
    #         # @ at the beginning of values not allowed as it is reserved for language tags
    #         # u"twitter_site": u"mfm_Kay",
    #         u"twitter_card": u"summary"
    #     }
    #     try:
    #         response = self.skb_client.save_entity(entity_dict=entity_data)
    #         assert False  # entityType must be set -> assertion error must be raised
    #     except AssertionError:
    #         assert True
    #     entity_data['entityType'] = 'AgentEntity'
    #     try:
    #         response = self.skb_client.save_entity_batch(
    #             entity_list=entity_data)
    #         assert False  # provenance must be set -> assertion error must be raised
    #     except AssertionError:
    #         assert True
    #     entity_data['provenance'] = 'agent_test_workflow_20191022'
    #     response = self.skb_client.save_entity(entity_dict=entity_data)
    #     assert response == 'http://weblyzard.com/skb/entity/agent/you_don_t_say'
    #     # Getting entity
    #     result = self.skb_client.get_entity(
    #         uri="http://weblyzard.com/skb/entity/agent/you_don_t_say")
    #     entity_type = entity_data.pop(u'entityType')
    #     provenance = entity_data.pop(u'provenance')  # provenance not returned
    #     assert entity_type in result[u'entityType']
    #     for k, v in entity_data.items():
    #         assert k in list(result['properties'].keys())
    #         assert v in result['properties'][k]['values']
    #     result = self.skb_client.get_entity(
    #         uri="agent:you_don_t_say")
    #     assert entity_type in result[u'entityType']
    #     for k, v in entity_data.items():
    #         assert k in list(result['properties'].keys())
    #         assert v in result['properties'][k]['values']
    #     result = self.skb_client.get_entity_by_property(
    #         property_name='url',
    #         property_value='http://www.youdontsayaac.com/hello-world-2/',
    #         entity_type='AgentEntity')
    #     assert isinstance(result, list)
    #     assert len(result) == 1
    #     assert entity_type in result[0][u'entityType']
    #     for k, v in entity_data.items():
    #         assert k in list(result[0]['properties'].keys())
    #         assert v in result[0]['properties'][k]['values']
    #     result = self.skb_client.get_entity_by_property(
    #         property_value='http://www.youdontsayaac.com/hello-world-2/')
    #     assert isinstance(result, list)
    #     assert len(result) == 1
    #     for k, v in entity_data.items():
    #         assert k in list(result[0]['properties'].keys())
    #         assert v in result[0]['properties'][k]['values']
    #
    # def test_save_entity_batch(self):
    #     entity_data = [{
    #         u"publisher": u"You Don't Say",
    #         u"title": u"Hello, world!",
    #         u"url": u"http://www.youdontsayaac.com/hello-world-2/",
    #         u"charset": u"UTF-8",
    #         u"thumbnail": u"https://s0.wp.com/i/blank.jpg",
    #         u"locale": u"en_US",
    #         u"last_modified": u"2014-07-15T18:46:42+00:00",
    #         u"page_type": u"article",
    #         u"published_date": u"2014-07-15T18:46:42+00:00",
    #         # @ at the beginning of values not allowed as it is reserved for language tags
    #         # u"twitter_site": u"twitter@mfm_Kay",
    #         u"twitter_card": u"summary"
    #     }]
    #     try:
    #         response = self.skb_client.save_entity_batch(
    #             entity_list=entity_data)
    #         assert False  # entityType must be set -> assertion error must be raised
    #     except AssertionError:
    #         assert True
    #     entity_data[0]['entityType'] = 'AgentEntity'
    #     try:
    #         response = self.skb_client.save_entity_batch(
    #             entity_list=entity_data)
    #         assert False  # provenance must be set -> assertion error must be raised
    #     except AssertionError:
    #         assert True
    #     entity_data[0]['provenance'] = 'agent_test_workflow_20191022'
    #     response = self.skb_client.save_entity_batch(entity_list=entity_data)
    #     assert(response['data'][0]['message'] in ['success', 'skipped'])
    #     assert response['data'][0]['uri'] == 'http://weblyzard.com/skb/entity/agent/you_don_t_say'
    #     # Getting entity
    #     result = self.skb_client.get_entity(
    #         uri="http://weblyzard.com/skb/entity/agent/you_don_t_say")
    #     entity_type = entity_data[0].pop(u'entityType')
    #     provenance = entity_data[0].pop(
    #         u'provenance')  # provenance not returned
    #     assert entity_type in result[u'entityType']
    #     for k, v in entity_data[0].items():
    #         assert k in list(result['properties'].keys())
    #         assert v in result['properties'][k]['values']
    #     result = self.skb_client.get_entity(
    #         uri="agent:you_don_t_say")
    #     for k, v in entity_data[0].items():
    #         assert k in list(result['properties'].keys())
    #         assert v in result['properties'][k]['values']
    #     result = self.skb_client.get_entity_by_property(
    #         property_name='url',
    #         property_value='http://www.youdontsayaac.com/hello-world-2/',
    #         entity_type='AgentEntity')
    #     assert isinstance(result, list)
    #     assert len(result) == 1
    #     for k, v in entity_data[0].items():
    #         assert k in list(result[0]['properties'].keys())
    #         assert v in result[0]['properties'][k]['values']
    #     result = self.skb_client.get_entity_by_property(
    #         property_value='http://www.youdontsayaac.com/hello-world-2/')
    #     assert isinstance(result, list)
    #     assert len(result) == 1
    #     for k, v in entity_data[0].items():
    #         assert k in list(result[0]['properties'].keys())
    #         assert v in result[0]['properties'][k]['values']


if __name__ == '__main__':
    unittest.main()
