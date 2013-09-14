#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Sep, 14 2013

.. module:: weblyzard_api.xml_content.translate
   :synopsis: translates deprecated versions of the weblyzardXml Format to the current version.

.. moduleauthor: Albert Weichselbraun <albert.weichselbraun@htwchur.ch>
'''

import logging
from lxml import etree

DOCUMENT_NAMESPACE  = {'wl': 'http://www.weblyzard.com/wl/2013#',
                       'dc': 'http://purl.org/dc/elements/1.1/',
                       'xml': 'http://www.w3.org/XML/1998/namespace',
                       }

SENTENCE_ATTRIBUTES = {
    'pos_tag_string': '{%s}%s' % (DOCUMENT_NAMESPACE['wl'], 'pos'), 
    'token_indices' : '{%s}%s' % (DOCUMENT_NAMESPACE['wl'], 'token'),
    'significance'  : '{%s}%s' % (DOCUMENT_NAMESPACE['wl'], 'significance'),
    'sem_orient'    : '{%s}%s' % (DOCUMENT_NAMESPACE['wl'], 'sem_orient'),
    'md5sum'        : '{%s}%s' % (DOCUMENT_NAMESPACE['wl'], 'id'),
}.items()

logger = logging.getLogger('wl_core.xml_content')


class WeblyzardXML2005(object):
    '''
    Translates the 
       http://www.weblyzard.com/wl/2005
    format into a
       http://www.weblyzard.com/wl/2013#
    compatible XML format.

    .. warning:: 
       This code solely relies on string substitutions and, therefore, is not
       robust against changes in the tag alignment.
    '''

    PAGE_START_TRANSLATION_TABLE = {
        'xmlns:wl="http://www.weblyzard.com/wl/2005"': 'xmlns:wl="http://www.weblyzard.com/wl/2013#" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:xml="http://www.w3.org/XML/1998/namespace"',
        'content_id="': 'wl:id="',
        'lang="'      : 'xml:lang="',
        'nilsimsa="'  : 'wl:nilsimsa="',
        'title="'     : 'dc:title="',
        'type="'      : 'dc:format="',}.items()

    PAGE_END_TRANSLATION_TABLE = { '</page>': '</wl:page>' }.items()

    SENTENCE_TRANSLATION_TABLE = { 
        'pos="'         : 'wl:pos="',
        'id="'          : 'wl:id="',
        'token="'       : 'wl:token="',
        'sem_orient="'  : 'wl:sem_orient="',
        'significance="': 'wl:significance="',
    }.items()

    @classmethod
    def translate(cls, xml_content):
        '''
        ... :param xml_content: the XML data to translate
        '''
        result = []
        for line in xml_content.split("\n"):
            if line.startswith('<page '):
                result.append(cls.translate_line(line, cls.PAGE_START_TRANSLATION_TABLE))
            elif line.startswith('</page>'):
                result.append(cls.translate_line(line, cls.PAGE_END_TRANSLATION_TABLE))
            elif line.startswith('<wl:sentence '):
                result.append(cls.translate_line(line, cls.SENTENCE_TRANSLATION_TABLE))
            elif line.startswith('</wl:sentence>'):
                continue
            else:
                raise ValueError(line)

        return '\n'.join(result)


    @classmethod
    def translate_line(cls, line, translation_table):
        '''
        .. :param line: the XML line to translate
        .. :param translation_table': a list of tuples of the form
                                      [(orig, translated), ... ] used for
                                      translating the line into the new
                                      format.
        '''
        for orig, translated in translation_table:
            line = line.replace(orig, translated)
        return line

