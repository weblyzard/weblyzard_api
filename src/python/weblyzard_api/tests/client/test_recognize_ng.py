#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Aug 30, 2016

.. codeauthor: max goebel <mcgoebel@gmail.com>
'''
import unittest

from weblyzard_api.client.recognize.ng import Recognize


class TestRecognizeNg(unittest.TestCase):

    SERVICE_URL = 'localhost:8086/rest'
    PROFILE_NAME = 'wl_dbpedia_en'
    DOCUMENTS = [{"id": "18",
                  "format": None,
                  "nilsimsa": "4afe0a56c114d94470928591f212e341248a09a5c990b2f288210a85e712af65",
                  "header": {},
                  "lang": "EN",
                  "sentences": [
                      {
                        "pos": None,
                        "dependency": None,
                        "token": None,
                        "significance": 0.0,
                        "md5sum": "b6e3ee36abdacf43e7f01cf7fb553557",
                        "is_title": False,
                        "text": "Helen of Troy Corp said it filed with the Securities and Exchange Commission a registration statement covering a 20 mln dlr issue of covertible subordinated debentures due 2007.",
                        "sem_orient": 0.0},
                      {
                          "pos": None,
                          "dependency": None,
                          "token": None, "significance": 0.0,
                          "md5sum": "cea05fd315805a421b6d562956ab8021",
                          "is_title": False,
                          "text": "Proceeds will be used for general corporate purposes, including possible repayment of bank debt, product development and possible acquisitions, Helen of Troy said.",
                          "sem_orient": 0.0},
                      {
                          "pos": None,
                          "dependency": None,
                          "token": None,
                          "significance": 0.0,
                          "md5sum": "085021e20c85b6bddef74cbeb90e2ea2",
                          "is_title": False,
                          "text": "The company named Drexel Burnham Lambert Inc as sole underwriter of the offering.",
                          "sem_orient": 0.0}],
                  "annotations": None}]

    def setUp(self):
        self.available_profiles = []
        self.client = Recognize(self.SERVICE_URL)
        self.service_is_online = self.client.is_online()
        if not self.service_is_online:
            print('WARNING: Webservice is offline --> not executing all tests!!')
            self.IS_ONLINE = False
            return

    def test_available_profiles(self):
        profiles = self.client.list_profiles()
        assert len(profiles) > 0

    def test_search_text(self):
        text = 'Vienna is the capital of Austria, Berlin is the capital of Germany. Linz also is in Austria'
        result = self.client.search_text(
            self.PROFILE_NAME, lang='en', text=text)
        assert len(result) == 6

    def test_annotate_document(self):
        for document in self.DOCUMENTS:
            annotations = self.client.search_document(profile_name=self.PROFILE_NAME,
                                                      document=document, limit=0)
            from pprint import pprint
            pprint(annotations)

            assert len(annotations) > 0
