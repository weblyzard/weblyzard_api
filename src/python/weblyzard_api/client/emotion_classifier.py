#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on April 07, 2021

@author: jakob <jakob.steixner@modul.ac.at>
'''

from weblyzard_api.client.opinion_mining import OpinionClient


class EmotionClassifierClient(OpinionClient):

    def get_polarity(self, content, content_format, extra_categories):
        """simplified API, currently no use for additional parameters"""
        return OpinionClient.get_polarity(self, content=content,
                                          content_format=content_format,
                                          extra_categories=extra_categories)