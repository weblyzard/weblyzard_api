#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import pytest
import unittest

from weblyzard_api.client.wl_rest_api import (WlDocumentRestApiClient,
                                              WlSearchRestApiClient)


@pytest.mark.skip(reason='requires base_url, username, password, left for documentation')
class TestWlSearchRestApiClient(unittest.TestCase):

    BASE_URL = ''
    USERNAME = ''
    PASSWORD = ''

    def test_auth_token(self):

        client = WlSearchRestApiClient(base_url=self.BASE_URL,
                                       username=self.USERNAME,
                                       password=self.PASSWORD)

        auth_token = client.get_auth_token(username=self.USERNAME,
                                           password=self.PASSWORD)
        assert auth_token

    def test_search_api(self):
        client = WlSearchRestApiClient(base_url=self.BASE_URL,
                                       username=self.USERNAME,
                                       password=self.PASSWORD)

        sources = ['climate.6.climate2_media']
        start_date = '2016-09-20'
        end_date = '2016-09-21'
        num_keywords = 5
        num_associations = 5
        auth_token = client.get_auth_token(username=self.USERNAME,
                                           password=self.PASSWORD)
        result = client.search_keywords(auth_token=auth_token,
                                        sources=sources,
                                        start_date=start_date,
                                        end_date=end_date,
                                        num_keywords=num_keywords,
                                        num_associations=num_associations)

        pass


@pytest.mark.skip(reason='requires service run on localhost')
class TestWlDocumentRestApiClient(unittest.TestCase):
    '''
    Test class for the WlRestApiClient class.
    '''
    TEST_PORTAL_NAME = 'test_weblyzard'
    TEST_MATVIEW_NAME = 'weblyzard_test'

    TEST_DOCUMENT = {
        'repository_id': 'repository',
        'uri': "the repository's uri",
        'title': 'document title',
        'content_type': 'text/plain',
        'content': """
            Google X's Project Wing concept was a unique take on the delivery drone: a single-winged UAV that took off and landed vertically. Despite extensive testing in Australia, the plan didn't work as well as the company hoped. In March this year Google X head Astro Teller announced the organization was working on a new design, and now, FAA documents show that two Google-built UAVs, codenamed the M2 and the B3, have been registered this month in the US. The M2 made the FAA registry on October 2nd, while the B3 was listed October 7th.
        """,
        'language_id': 'en',

    }
    test_dict_content = {
        'uri': "the repository's uri",
        'title': "document title",
        'repository_id': 'repository',
        'content_type': 'text/plain',
        'content': 'Therefore we could show that "x>y" and "y<z.".',
    }

    def setUp(self):
        # TODO Change this to the running instance
        self.client = WlDocumentRestApiClient("http://localhost:5001")
        print("+++ INFO: Sending requests to %s +++" % self.client.base_url)

    def compare_with_base(self, base_dict, extended_dict):
        '''
        Takes two dicts and returns true iff all key:value pairs
        ocurring in base_dict are identical in extended_dict. 
        Additional key:value pairs in extended_dict are allowed.
        '''
        for key in base_dict:
            try:
                if extended_dict[key] != base_dict[key]:
                    return False
            except:
                return False
        return True

    def test_status(self):
        assert self.client.get_status()['status'] == 'OK'

    def test_check_documet(self):
        result = self.client.check_document(self.test_dict_content)
        assert result == {u'status': u'success'}

    def test_annotate_documet(self):
        result = self.client.annotate_document(
            self.test_dict_content, ['sem_orient_ng', 'jesaja'])
        del result['meta_data']['published_date']
        assert result['sentences'] == [
            {
                "dep_tree": "1:NMOD -1:ROOT",
                "id": "9b6496ed96416839b561e2d3e64579bf",
                "is_title": True,
                "pos_list": "NN NN",
                "tok_list": "0,8 9,14",
                "value": "document title"
            },
            {
                "dep_tree": "2:ADV 2:SBJ 16:DEP 2:VC 3:ADV 4:P 4:COORD 8:MNR 6:CONJ 16:DEP 16:DEP 12:P 13:AMOD 14:NMOD 16:P 16:DEP -1:ROOT",
                "id": "6e4c1420b2edaa374ff9d2300b8df31d",
                "is_title": False,
                "pos_list": "RB PRP MD VB IN `` CC JJR JJ `` CC `` NN JJR CD `` .",
                "tok_list": "0,9 10,12 13,18 19,23 24,28 29,30 30,31 31,32 32,33 33,34 35,38 39,40 40,41 41,42 42,44 44,45 45,46",
                "value": "Therefore we could show that \"x>y\" and \"y<z.\"."
            }
        ]
        assert result == {
            "language_id": "en",
            "meta_data": {
                "polarity": 0.0,
            },
            "repository_id": "repository",
            "sentences": [
                {
                    "dep_tree": "1:NMOD -1:ROOT",
                    "id": "9b6496ed96416839b561e2d3e64579bf",
                    "is_title": True,
                    "pos_list": "NN NN",
                    "tok_list": "0,8 9,14",
                    "value": "document title"
                },
                {
                    "dep_tree": "2:ADV 2:SBJ 16:DEP 2:VC 3:ADV 4:P 4:COORD 8:MNR 6:CONJ 16:DEP 16:DEP 12:P 13:AMOD 14:NMOD 16:P 16:DEP -1:ROOT",
                    "id": "6e4c1420b2edaa374ff9d2300b8df31d",
                    "is_title": False,
                    "pos_list": "RB PRP MD VB IN `` CC JJR JJ `` CC `` NN JJR CD `` .",
                    "tok_list": "0,9 10,12 13,18 19,23 24,28 29,30 30,31 31,32 32,33 33,34 35,38 39,40 40,41 41,42 42,44 44,45 45,46",
                    "value": "Therefore we could show that \"x>y\" and \"y<z.\"."
                }
            ],
            "title": "document title",
            "uri": "the repository's uri"
        }

    def test_annotate_document_sentiment_ng(self):
        test_document_de = {
            'repository_id': 'repository',
            'uri': "the repository's uri",
            'title': 'Dokumenttitel',
            'content_type': 'text/plain',
            'content': """Wenn die Sprache nicht richtig erkannt wird oder immer neutral zurückgeliefert wird, dann ist das sehr schlecht und ein Fehler.""",
            'language_id': 'de',
        }
        test_document_de_ascii = {
            'repository_id': 'repository',
            'uri': "the repository's uri",
            'title': 'Dokumenttitel',
            'content_type': 'text/plain',
            'content': """Wenn die Sprache nicht richtig erkannt wird oder immer neutral retourniert wird, dann ist das sehr schlecht und ein Fehler.""",
            'language_id': 'de',
        }
        test_document_en = {
            'repository_id': 'repository',
            'uri': "the repository's uri",
            'title': 'Document title',
            'content_type': 'text/plain',
            'content': """An excellent text as input!""",
            'language_id': 'en',
        }
        test_document_fr = {
            'repository_id': 'repository',
            'uri': "the repository's uri",
            'title': 'Titre du document',
            'content_type': 'text/plain',
            'content': """C'est un texte grave.""",
            'language_id': 'fr',
        }
        result = self.client.annotate_document(
            test_document_en, ['sem_orient_ng'])
        assert result['meta_data']['polarity'] in [1.0, 'positive']
        print(result['meta_data']['polarity'])
        assert result['language_id'] == 'en'
        result = self.client.annotate_document(
            test_document_fr, ['sem_orient_ng'])
        assert result['meta_data']['polarity'] in [-1.0, 'negative']
        assert result['language_id'] == 'fr'
        result = self.client.annotate_document(
            test_document_de_ascii, ['sem_orient_ng'])
        assert result['meta_data']['polarity'] in [-1.0, 'negative']
        assert result['language_id'] == 'de'
        result = self.client.annotate_document(
            test_document_de, ['sem_orient_ng'])
        assert result['meta_data']['polarity'] in [-1.0, 'negative']
        assert result['language_id'] == 'de'

    def notest_crud_document(self):
        '''
        Tests all CRUD operations for document in the following
        order:
            * Create document and get content_id.
            * Read the document, check that the content is correct.
            * Update the document with a minor change.
            * Read again and assert that the changes were accepted/\
                    persisted.
            * Delete the document.
            * Try to read the document and fail.
        '''
        document = json.dumps(self.TEST_DOCUMENT)
        portal_name = self.TEST_PORTAL_NAME
        # CREATE
        created_response = self.client.add_document(portal_name=portal_name,
                                                    document=document)
        assert isinstance(created_response, dict)
        assert '_id' in created_response
        assert created_response['created'] == True
        assert 'title' not in created_response
        content_id = created_response['_id']

        # READ
        read1_response = self.client.retrieve_document(portal_name=portal_name,
                                                       content_id=content_id)
        assert isinstance(read1_response, dict)
        print(read1_response)
        assert read1_response['_id'] == content_id
        assert read1_response['repository_id'] == 'repository'
        assert read1_response['title'] == 'document title'
        assert self.compare_with_base(self.TEST_DOCUMENT, read1_response)

        # UPDATE
        updated_testdict = dict(self.TEST_DOCUMENT)
        updated_testdict['title'] = 'updated document title'
        updated_document = json.dumps(updated_testdict)
        updated_response = self.client.update_document(portal_name=portal_name,
                                                       content_id=content_id,
                                                       document=updated_document)
        assert isinstance(updated_response, dict)
        print(updated_response)
        assert updated_response['created'] == False
        assert updated_response['_id'] == content_id
        assert 'title' not in updated_response

        # READ again
        read2_response = self.client.retrieve_document(portal_name=portal_name,
                                                       content_id=content_id)
        assert isinstance(read2_response, dict)
        print(read2_response)
        assert read2_response['_id'] == content_id
        assert read2_response['repository_id'] == 'repository'
        assert read2_response['title'] == 'updated document title'
        assert self.compare_with_base(updated_testdict, read2_response)

        # DELETE
        delete_response = self.client.delete_document(portal_name=portal_name,
                                                      content_id=content_id)
        assert isinstance(delete_response, dict)
        print(delete_response)
        assert delete_response['_id'] == content_id
        assert delete_response['deleted'] == True
        assert len(delete_response) == 2

        # READ and fail
        read3_response = self.client.retrieve_document(portal_name=portal_name,
                                                       content_id=content_id)
        print(read3_response)
        assert False


if __name__ == '__main__':
    unittest.main()
