#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
**webLyzard web service clients**

.. codeauthor:: Albert Weichselbraun <albert.weichselbraun@htwchur.ch>
.. codeauthor:: Heinz-Peter Lang <lang@weblyzard.com>
'''
from __future__ import unicode_literals
from os import getenv

WEBLYZARD_API_URL = getenv("WEBLYZARD_API_URL") or "http://localhost:8080"
WEBLYZARD_API_USER = getenv("WEBLYZARD_API_USER")
WEBLYZARD_API_PASS = getenv("WEBLYZARD_API_PASS")

OGER_API_URL = getenv("OGER_API_URL")




