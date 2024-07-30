import logging
from pprint import pprint

from weblyzard_api.client.triplestore import TriplestoreWrapper2

logger = logging.getLogger(__name__)


class QleverWrapper(TriplestoreWrapper2):
    """
    Built upon the SPARQLWrapper for accessing Qlever.
    """

    def __init__(self, sparql_endpoint, debug=False):
        super().__init__(sparql_endpoint=sparql_endpoint,
                         debug=debug)

    @staticmethod
    def from_config(host, port, dataset: str):
        return QleverWrapper(sparql_endpoint=f'{host}:{port}/{dataset}',
                             debug=False)
