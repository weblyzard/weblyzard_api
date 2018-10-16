#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest
import json

from weblyzard_api.model.document import Document


class TestJSON2018Parser(unittest.TestCase):

    JSON_2018 = """
    {
    "id": 7,
    "format": "text/html",
    "lang": "EN",
    "header": {},
    "annotations": [],
    "nilsimsa": "1404e487721ca21e08c2141155621022f39a991640a419064123b812a30f2acc",
    "content": "1 Corinthians 13:4-7\\nLove is patient, love is kind. It does not envy, it does not boast, it is\\nnot proud.",
    "partitions": {
        "TITLE": [{
            "@type": "CharSpan",
            "start": 0,
            "end": 20
        }],
        "BODY": [{
            "@type": "CharSpan",
            "start": 21,
            "end": 104
        }],
        "LINE": [{
            "@type": "CharSpan",
            "start": 0,
            "end": 20
        }, {
            "@type": "CharSpan",
            "start": 21,
            "end": 94
        }, {
            "@type": "CharSpan",
            "start": 95,
            "end": 106
        }],
        "SENTENCE": [{
            "@type": "SentenceCharSpan",
            "start": 0,
            "end": 20,
            "id": "asdfasdmasdnsd23232",
            "semOrient": 1.0,
            "significance": 0.1231
        }, {
            "@type": "SentenceCharSpan",
            "start": 21,
            "end": 51,
            "id": "asdfasdmasdnsd23233",
            "semOrient": 1.0,
            "significance": 0.1231
        }, {
            "@type": "SentenceCharSpan",
            "start": 52,
            "end": 106,
            "id": "asdfasdmasdnsd23231",
            "semOrient": 1.0,
            "significance": 0.1231
        }],
        "TOKEN": [{
            "@type": "TokenCharSpan",
            "start": 0,
            "end": 1,
            "pos": "CD",
            "dependency": {
                "parent": 2,
                "label": "NMOD"
            }
        }, {
            "@type": "TokenCharSpan",
            "start": 2,
            "end": 13,
            "pos": "NNP",
            "dependency": {
                "parent": 2,
                "label": "NMOD"
            }
        }, {
            "@type": "TokenCharSpan",
            "start": 14,
            "end": 18,
            "pos": "CD",
            "dependency": {
                "parent": 3,
                "label": "NMOD"
            }
        }, {
            "@type": "TokenCharSpan",
            "start": 18,
            "end": 20,
            "pos": "CD",
            "dependency": {
                "parent": -1,
                "label": "ROOT"
            }
        }, {
            "@type": "TokenCharSpan",
            "start": 21,
            "end": 25,
            "pos": "NN",
            "dependency": {
                "parent": 5,
                "label": "SBJ"
            }
        }, {
            "@type": "TokenCharSpan",
            "start": 26,
            "end": 28,
            "pos": "VBZ",
            "dependency": {
                "parent": -1,
                "label": "ROOT"
            }
        }, {
            "@type": "TokenCharSpan",
            "start": 29,
            "end": 36,
            "pos": "NN",
            "dependency": {
                "parent": 5,
                "label": "PRD"
            }
        }, {
            "@type": "TokenCharSpan",
            "start": 36,
            "end": 37,
            "pos": ",",
            "dependency": {
                "parent": 5,
                "label": "P"
            }
        }, {
            "@type": "TokenCharSpan",
            "start": 37,
            "end": 42,
            "pos": "NN",
            "dependency": {
                "parent": 5,
                "label": "PRD"
            }
        }, {
            "@type": "TokenCharSpan",
            "start": 43,
            "end": 25,
            "pos": "VBZ",
            "dependency": {
                "parent": 5,
                "label": "CONJ"
            }
        }, {
            "@type": "TokenCharSpan",
            "start": 46,
            "end": 50,
            "pos": "NN",
            "dependency": {
                "parent": 9,
                "label": "PRD"
            }
        }, {
            "@type": "TokenCharSpan",
            "start": 50,
            "end": 51,
            "pos": ".",
            "dependency": {
                "parent": 5,
                "label": "P"
            }
        }, {
            "@type": "TokenCharSpan",
            "start": 52,
            "end": 54,
            "pos": "PRP",
            "dependency": {
                "parent": 12,
                "label": "SBJ"
            }
        }, {
            "@type": "TokenCharSpan",
            "start": 55,
            "end": 59,
            "pos": "VBZ",
            "dependency": {
                "parent": -1,
                "label": "ROOT"
            }
        }, {
            "@type": "TokenCharSpan",
            "start": 60,
            "end": 63,
            "pos": "RB",
            "dependency": {
                "parent": 12,
                "label": "ADV"
            }
        }, {
            "@type": "TokenCharSpan",
            "start": 64,
            "end": 68,
            "pos": "VB",
            "dependency": {
                "parent": 12,
                "label": "VC"
            }
        }, {
            "@type": "TokenCharSpan",
            "start": 68,
            "end": 69,
            "pos": ",",
            "dependency": {
                "parent": 17,
                "label": "P"
            }
        }, {
            "@type": "TokenCharSpan",
            "start": 70,
            "end": 72,
            "pos": "PRP",
            "dependency": {
                "parent": 17,
                "label": "SBJ"
            }
        }, {
            "@type": "TokenCharSpan",
            "start": 73,
            "end": 77,
            "pos": "VBZ",
            "dependency": {
                "parent": 12,
                "label": "PRD"
            }
        }, {
            "@type": "TokenCharSpan",
            "start": 78,
            "end": 81,
            "pos": "RB",
            "dependency": {
                "parent": 17,
                "label": "ADV"
            }
        }, {
            "@type": "TokenCharSpan",
            "start": 82,
            "end": 87,
            "pos": "VB",
            "dependency": {
                "parent": 17,
                "label": "VC"
            }
        }, {
            "@type": "TokenCharSpan",
            "start": 87,
            "end": 88,
            "pos": ",",
            "dependency": {
                "parent": 22,
                "label": "P"
            }
        }, {
            "@type": "TokenCharSpan",
            "start": 89,
            "end": 91,
            "pos": "PRP",
            "dependency": {
                "parent": 22,
                "label": "SBJ"
            }
        }, {
            "@type": "TokenCharSpan",
            "start": 92,
            "end": 94,
            "pos": "VBZ",
            "dependency": {
                "parent": 12,
                "label": "PRD"
            }
        }, {
            "@type": "TokenCharSpan",
            "start": 95,
            "end": 98,
            "pos": "RB",
            "dependency": {
                "parent": 22,
                "label": "ADV"
            }
        }, {
            "@type": "TokenCharSpan",
            "start": 99,
            "end": 104,
            "pos": "JJ",
            "dependency": {
                "parent": 22,
                "label": "PRD"
            }
        }, {
            "@type": "TokenCharSpan",
            "start": 104,
            "end": 105,
            "pos": ".",
            "dependency": {
                "parent": 12,
                "label": "P"
            }
        }]
    }
}
"""

    def test_from_json(self):
        document = Document.from_json(self.JSON_2018)
        sentences = document.get_sentences()
        assert len(sentences) == 3

    def test_full(self):
        document = Document.from_json(self.JSON_2018)
        result = json.loads(document.to_json())

        expected_json = json.loads(self.JSON_2018)
        from pprint import pprint
        pprint(json.dumps(expected_json))
        pprint('================')
        pprint(json.dumps(result))
        assert result == expected_json


if __name__ == '__main__':
    unittest.main()
