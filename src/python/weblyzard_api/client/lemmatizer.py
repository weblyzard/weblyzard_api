#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on November 14, 2019

@author: jakob <jakob.steixner@modul.ac.at>
'''
from itertools import chain

from typing import Tuple, List, Optional

from weblyzard_api.client import MultiRESTClient
from weblyzard_api.model import Sentence


class LemmatizerClient(MultiRESTClient):
    VERSION: float = 1.0
    LEMMATIZER_PATH: str = f'{VERSION}/skb/lemmata'

    def __init__(self, url: str):
        """

        :param url: Url of the lemmatizer web service
        """
        self.url = url
        MultiRESTClient.__init__(self, service_urls=url)

    def get_unique_lemmas_string(self, language: str, plain_text: str='',
                                 forms:Optional[list]=None,
                                 **kwargs):
        """
        Returns dict of term: lemma but only if the term has a unique lemma,
        independent of pos.
        :param language:
        :param plain_text:
        :param kwargs:
        :return: dict term: lemma, str:str
        """
        res = self._get_lemmas_plaintext(language=language,
                                         plain_text=plain_text,
                                         forms=forms, **kwargs)
        return {k: v['lemma'] for k, v in res.get('result', {}).items() if
                'lemma' in v}

    def _get_lemmas_plaintext(self, language: str, plain_text: str,
                              forms: Optional[list]=None, **kwargs):
        doc = {
            'lang': language,
            'plain_text': plain_text,
            'return_base_forms_only': True,
            'forms': forms

        }
        doc = {k: v for k, v in doc.items() if v is not None}
        if kwargs:
            doc.update(kwargs)

        return self.request(path=self.LEMMATIZER_PATH, parameters=doc)

    def _get_lemmas_tuples(self, language: str,
                           form_pos_pairs: List[Tuple[str, str]],
                           check_unique: bool=True, **kwargs: dict):
        """
        Helper function for Sentence input
        :param language:
        :param form_pos_pairs: list of tuples. Pos can be either generic
            full names (noun, verb, adjective), or language specific treebank
            tag, which the service will attempt to map to the former
        :param kwargs:
        :param check_unique: if True, ignore ambiguous terms, values in
            returned dict are strings; if False, include ambiguous terms,
            values in returned dict are lists (also for unambiguous terms for
            consistency)
        :return: dict with term: lemma or term: [lemmas]
        """
        doc = {
            'lang': language,
            'form_pos_pairs': form_pos_pairs,
            'return_base_forms_only': True,
            'check_unique': check_unique

        }
        if kwargs:
            doc.update(kwargs)

        return self.request(path=self.LEMMATIZER_PATH, parameters=doc)

    def get_all_lemmas(self, language: str, plain_text: str,
                       forms: Optional[list]=None, **kwargs: dict):
        """
        Get lemmas, including potentially ambiguous ones
        :param language:
        :param plain_text:
        :param kwargs: additional parameters passed to API
        :return: dict with terms as keys, lists of candidate lemmas as values
        """
        raw = self._get_lemmas_plaintext(language=language,
                                         plain_text=plain_text,
                                         forms=forms, **kwargs)
        res = {}
        for term, termresult in raw.get('result', {}).items():
            if 'lemma' in termresult:
                res[term] = [termresult['lemma']]
            elif 'AMBIGUOUS' in termresult:
                res[term] = list(chain(*termresult['AMBIGUOUS'].values()))
        return res

    def get_lemmas_annotated_sentence(self, language: str,
                                      sentence: Sentence,
                                      check_unique: bool=False,
                                      **kwargs):
        """
        Function allowing weblyzard_api.model.Sentence to be directly input,
        performing pos-specific lemma lookup
        :param language: iso code for language
        :param sentence: sentence to process
        :param check_unique:
        :param kwargs:
        :return: dict with '{term}@{pos} as keys, lists of candidate lemmas as
            values if `check_unique==False`, strings as values if
            `check_unique==True`; terms where lemma lookup fails, or with
            multiple candidates if `check_unique==True`, are left out
        :rtype dict
        """
        if not sentence.pos or not sentence.token:
            # fallback to plaintext methods if sentence.token and/or .pos empty
            self.get_unique_lemmas_string(language=language,
                                          plain_text=sentence.value, **kwargs)

        token_pairs = list(zip(sentence.tokens, sentence.pos_tags))
        raw = self._get_lemmas_tuples(language=language,
                                      form_pos_pairs=token_pairs,)

        result = {}
        for k, v in raw.get('result', {}).items():
            if 'lemma' in v:
                if check_unique:
                    result[k] = v['lemma']
                else:
                    result[k] = [v['lemma']]
            if 'AMBIGUOUS' in v and not check_unique:
                result[k] = v['AMBIGUOUS']

        return result

    def expand_lemma(self, *args, **kwargs):
        """todo: Function to get alternate forms too"""
        raise NotImplementedError
