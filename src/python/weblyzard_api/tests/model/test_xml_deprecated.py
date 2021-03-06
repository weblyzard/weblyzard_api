#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Jan 25, 2018

.. codeauthor: Max Goebel <goebel@weblyzard.com>
'''
from __future__ import unicode_literals
import unittest

from weblyzard_api.model.parsers.xml_deprecated import XMLDeprecated


class TestXMLDeprecated(unittest.TestCase):

    def test(self):
        xml = ''' 
            <wl:page xmlns:wl="http://www.weblyzard.com/" content_id="228557824" content_type="text/html" lang="DE" title="Der ganze Wortlaut: Offener Brief an Niko Pelinka  | Heute.at   ">
                <wl:sentence id="7e985ffb692bb6f617f25619ecca39a9"><![CDATA[Der ganze Wortlaut]]></wl:sentence>
                <wl:sentence id="7e985ffb692bb6f617f25619ecca39a9"><![CDATA[Der ganze Wortlaut]]></wl:sentence>
            </wl:page> '''

        attributes, sentences, title_annotations, body_annotations, features, relations = XMLDeprecated.parse(xml)
        assert len(attributes) == 4
        assert len(sentences) == 1
        for sent in sentences:
            assert 'id' not in sent
            assert 'md5sum' in sent


if __name__ == '__main__':
    unittest.main()
