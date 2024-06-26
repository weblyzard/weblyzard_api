from __future__ import print_function
from __future__ import unicode_literals

import logging
from pprint import pprint

from weblyzard_api.client.triplestore import TriplestoreWrapper2

logger = logging.getLogger(__name__)


class BlazegraphWrapper(TriplestoreWrapper2):
    """
    Built upon the SPARQLWrapper for accessing blazegraph.
    """
    def __init__(self, sparql_endpoint, debug=False):
        super().__init__(sparql_endpoint=sparql_endpoint,
                         debug=debug)

    @staticmethod
    def from_config(host, port):
        path = 'bigdata/namespace/wdq/sparql'  # default query path
        return BlazegraphWrapper(sparql_endpoint=f'{host}:{port}/{path}',
                                 debug=False)
