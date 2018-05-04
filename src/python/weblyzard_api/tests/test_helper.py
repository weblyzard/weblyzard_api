#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 19.04.2013

:author: heinz-peterlang

Test helper module to load test files from TEST_DATA directory

'''
import os
import pickle


def get_test_data(fn, data_dir=None, return_file=False):
    with open(get_full_path(fn, data_dir), 'rb') as f:

        if return_file:
            return f

        if fn.lower().endswith('.pickle'):
            content = pickle.load(f)
        else:
            content = f.read()

        return content


def get_full_path(fn, data_dir=None):
    data_dir = data_dir if data_dir else get_test_data_dir()
    return os.path.join(data_dir, fn)


def get_test_data_dir():
    ''' returns the test_data_directory 

    Usage:
    >>> get_test_data_dir() # doctest: +ELLIPSIS
    '.../wl_mirroring/test/data'
    '''
    print(os.path.abspath(os.path.join(os.path.dirname(__file__), 'data')))
    return os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))


if __name__ == '__main__':
    import doctest
    doctest.testmod()
