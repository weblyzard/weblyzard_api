#!/usr/bin/python
# -*- coding: utf-8 -*-

import pytest
import unittest

from os import environ
from dotenv import load_dotenv
load_dotenv()

from weblyzard_api.client.wlt_api_client import WltSearchRestApiClient


@pytest.mark.skip(reason='requires base_url, username, password, left for documentation')
class TestWlSearchRestApiClient(unittest.TestCase):

    BASE_URL = environ['BASE_URL']
    USERNAME = environ['USERNAME']
    PASSWORD = environ['PASSWORD']

    def test_auth_token(self):

        client = WltSearchRestApiClient(base_url=self.BASE_URL,
                                        username=self.USERNAME,
                                        password=self.PASSWORD)

        auth_token = client.get_auth_token(username=self.USERNAME,
                                           password=self.PASSWORD)
        assert auth_token

    def test_search_api(self):
        client = WltSearchRestApiClient(base_url=self.BASE_URL,
                                        username=self.USERNAME,
                                        password=self.PASSWORD)

        sources = ['api.weblyzard.com/news_en']
        start_date = '2024-04-20'
        end_date = '2024-04-21'
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

        fields = [
            "document.contentid",
            "document.score",
            "document.title",
            "document.url",
            "document.date",
            "document.source_identifier"
        ]
        result = [d for d in client.search_documents(
                                            auth_token=auth_token,
                                            fields=fields,
                                            sources=sources,
                                            start_date=start_date,
                                            end_date=end_date,
                                            source_ids=['http:cnn.com'])]
        expected_fields = ["contentid", "score", "title", "url", "date", "source_identifier"]
        for doc in result:
            assert all([field in doc for field in expected_fields])
            assert doc['source_identifier'] == 'http:cnn.com'

        pass


if __name__ == '__main__':
    unittest.main()
