#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Jun 24, 2012

@author: heinz-peterlang
'''
from weblyzard_api.model.parsers.xml_2005 import XML2005


class XMLDeprecated(XML2005):

    SUPPORTED_NAMESPACE = 'http://www.weblyzard.com/'
    VERSION = 'deprecated'
