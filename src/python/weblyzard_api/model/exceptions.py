#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Jan 25, 2018

.. codeauthor: Max Goebel <goebel@weblyzard.com>
'''


class MissingContentException(Exception):
    '''
    Exception class thrown if a JSON document misses required fields.
    '''
    pass


class MissingFieldException(Exception):
    '''
    Exception class thrown if a JSON document misses required fields.
    '''
    pass


class UnsupportedValueException(Exception):
    '''
    Exception class thrown if a JSON document contains an unsupported value.
    '''
    pass


class UnexpectedFieldException(Exception):
    '''
    Exception class thrown if a JSON document contains an unexpected field.
    '''
    pass


class MalformedJSONException(Exception):
    '''
    Exception to throw if the json.loads function fails or the JSON is
    otherwise ill formatted.
    '''
    pass
