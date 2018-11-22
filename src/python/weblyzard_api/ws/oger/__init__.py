#!/usr/bin/env python3
# coding:utf-8
'''
NER Web service
'''

from flask import request, Response, Flask
from json import loads, dumps
from weblyzard_api.client import OGER_API_URL
from weblyzard_api.client.ontogene import Oger

app = Flask(__name__)

__author__ = "Albert Weichselbraun, Adrian Brasoveanu"
__copyright__ = "Copyright (C) 2018 Albert Weichselbraun, Adrian Brasoveanu"
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Adrian Brasoveanu"
__email__ = "adrian.brasoveanu@modul.ac.at"
__status__ = "Prototype"

@app.route("/")
def index():
    return "Hello"


@app.route("/get_ner", methods=['POST'])
def get_text_call():
    # retrieve the document dictionary from the request data
    document = loads(request.data)

    # please compute the annotations here
    url = OGER_API_URL
    client = Oger(url)
    docid = document['id']
    doctext = document['text']
    
    annotations = client.annotate_text(docid, doctext)

    # add your annotations to the document and return them
    document['annotations'] = annotations
    return Response(dumps(document), mimetype='application/json')


if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=5002)