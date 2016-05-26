#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
Jesaja Keyword Service - Example
Written by Albert Weichselbraun <weichselbraun@weblyzard.com>
'''

from sys import path
from os.path import join as os_join, dirname
from glob import glob
from cPickle import loads, load, dump
from gzip import GzipFile
from json import dump as jdump, load as jload
from time import time

from weblyzard_api.client.jesaja_ng import JesajaNg as Jesaja
from weblyzard_api.client.jeremia import Jeremia
from weblyzard_api.xml_content import XMLContent
from eWRT.util.module_path import get_resource

MATVIEW_NAME  = 'example'
PROFILE_NAME  = "example_profile"
STOPLIST_NAME = "example_stoplist"
STOPLIST_FILE = "example_stoplist.txt.gz"

PROFILE = { 'valid_pos_tags'                 : ['NN', 'P', 'ADJ'],
            'min_phrase_significance'        : 1.0,
            'num_keywords'                   : 7,
            'keyword_algorithm'              : 'com.weblyzard.backend.jesaja.algorithm.keywords.YatesKeywordSignificanceAlgorithm',
            'min_token_count'                : 2,
            'skip_underrepresented_keywords' : True,
            'stoplists'                      : [STOPLIST_NAME],
          }



def read_corpus_files(path):
    ''' reads the corpus documents from the given path '''
    corpus_documents = []
    for fname in glob(path):
        doc = {'id': fname,
               'body': GzipFile(fname).read().strip(),
               'title': '',
               'format': 'text/plain'}
        corpus_documents.append(doc)

    return corpus_documents

def get_weblyzard_xml_documents(corpus_documents):
    '''
    Performs the pre-processing of the corpus documents (i.e. text
    files are converted into the weblyzard XML format.
    '''
    jeremia = Jeremia()
    result = [doc['xml_content'] for doc in jeremia.submit_documents(corpus_documents)]
    return result

if __name__ == '__main__':

    print "Reading corpus..."
    CORPUS_PATH = os_join(dirname(__file__), '../corpus', '*.txt.gz')
    corpus_documents = read_corpus_files(CORPUS_PATH)

    print "Pre-processing corpus..."
    xml_corpus_documents = get_weblyzard_xml_documents(corpus_documents)

    print "Configuring keyword service..."
    jesaja = Jesaja()
    jesaja.set_stoplist(STOPLIST_NAME, [stopword.strip() for stopword in GzipFile(STOPLIST_FILE)])
    jesaja.set_keyword_profile(PROFILE_NAME, PROFILE)
    jesaja.set_matview_profile(matview_id=MATVIEW_NAME, profile_name=PROFILE_NAME)

    # check whether we have already shards available for the given matview
    if not jesaja.has_corpus(matview_id=MATVIEW_NAME):
        print "Uploading reference corpus..."
        # we try to rotate the corpus shards until enough documents have been
        # uploaded
        while jesaja.rotate_shard(MATVIEW_NAME) == 0:
            print " Adding corpus..."
            jesaja.add_documents(MATVIEW_NAME, xml_corpus_documents)

    print "Computing keywords..."
    result = jesaja.get_keywords(MATVIEW_NAME, xml_corpus_documents)

    with GzipFile("results.json.gz", "w") as f:
        jdump(result, f, indent=True)
