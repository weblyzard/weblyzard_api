'''
The webLyzard API package.

.. codeauthor:: Albert Weichselbraun <weichselbraun@weblyzard.com>
.. codeauthor:: Heinz-Peter Lang <lang@weblyzard.com>
'''
from __future__ import unicode_literals

from json import JSONEncoder


def _default(self, obj):
    return getattr(obj.__class__, "__json__", _default.default)(obj)


_default.default = JSONEncoder().default
JSONEncoder.default = _default