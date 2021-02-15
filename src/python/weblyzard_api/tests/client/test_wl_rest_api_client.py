#!/usr/bin/python
# -*- coding: utf-8 -*-

import pytest
import unittest
from weblyzard_api.client.wlt_api_client import WltSearchRestApiClient


@pytest.mark.skip(reason='requires base_url, username, password, left for documentation')
class TestWlSearchRestApiClient(unittest.TestCase):

    BASE_URL = ''
    USERNAME = ''
    PASSWORD = ''

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


if __name__ == '__main__':
    unittest.main()
