#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Jan 25, 2018

.. codeauthor: Max Goebel <goebel@weblyzard.com>
'''
from weblyzard_api.model.parsers.xml_2013 import XML2013


class Document(object):

    def __init__(self, content_id, url, content_model=None, metadata={},
                 annotations={}, features={}, relations={}):
        ''' '''
        self.content_id = content_id
        self.url = url
        self.content_model = content_model
        self.metadata = metadata
        self.annotations = annotations
        self.features = features
        self.relations = relations

    def to_xml(self, ignore_title=False, xml_version=XML2013.VERSION):
        ''' '''
        if not hasattr(self, 'features'):
            self.features = {}

        if not hasattr(self, 'relations'):
            self.relations = {}

        titles = self.titles
        if ignore_title:
            titles = []

        return self.SUPPORTED_XML_VERSIONS[xml_version].dump_xml(
            titles=titles,
            attributes=self.attributes,
            sentences=self.sentences,
            annotations=self.annotations,
            features=self.features,
            relations=self.relations)
