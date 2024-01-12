#!/usr/bin/env python
# encoding: utf-8

from setuptools import setup, find_packages
from setuptools.command import sdist

setup(
    name='weblyzard_api',
    version='3.0.0-dev',
    description=' Web services for weblyzard',
    author='Albert Weichselbraun, Heinz-Peter Lang, Max Göbel and Philipp Kuntschik',
    author_email='weichselbraun@weblyzard.com',
    packages=find_packages('src/python'),
    package_dir={'': 'src/python'},
    install_requires=['future',
                      'nose',
                      'lxml',
                      'requests[security]>=2.13,<3',
                      'pytest',
                      'sparqlwrapper'],
    classifiers=[
        'Programming Language :: Python :: 3.10',
                 'Programming Language :: Python :: 3.9',
                 'Programming Language :: Python :: 3.8',
                 'Programming Language :: Python :: 3.7',
                 'Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: 3 :: Only'],
    zip_safe=False,
    include_package_data=True,
    scripts=['src/python/weblyzard_api/client/openrdf/wl_upload_repository.py', ]
)
