#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 07.04.2014

@author: heinz-peterlang
'''
from weblyzard_api.xml_content.parsers import XMLParser


class XML2005(XMLParser):

    VERSION = 2005

    SUPPORTED_NAMESPACE = 'http://www.weblyzard.com/wl/2005'

    DOCUMENT_NAMESPACES = {'wl': SUPPORTED_NAMESPACE}

    ATTR_MAPPING = {'content_id': ('content_id', None),
                    'source_id': ('source_id', None),
                    'content_type': ('content_type', None),
                    'title': ('title', None),
                    'url': ('url', None),
                    'nilsimsa': ('nilsimsa', None),
                    'jonas_type': ('jonas_type', None),
                    'title_de': ('title_de', None),
                    'title_en': ('title_en', None),
                    'title_fr': ('title_fr', None),
                    'lang': ('lang', None),
                    }

    SENTENCE_MAPPING = {'pos': ('pos_tags', None),
                        'md5sum': ('md5sum', None),
                        'content_id': ('content_id', None),
                        'dependency': ('dependency', None),
                        'token': ('token', None),
                        'significance': ('significance', None),
                        'is_title': ('is_title', None),
                        'sem_orient': ('sem_orient', None)}

    FEATURE_MAPPING = {}

    RELATION_MAPPING = {}

    @classmethod
    def pre_xml_dump(cls, titles, attributes, sentences):

        if not 'title' in attributes:
            attributes['title'] = ' '.join([t.value for t in titles])

        return attributes, titles + sentences
