#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Feb, 27 2013

.. codeauthor: Heinz-Peter Lang <lang@weblyzard.com>
.. codeauthor: Albert Weichselbraun <Weichselbraun@weblyzard.com>
.. codeauthor: Fabian Fischer <fabian.fischer@modul.ac.at>

Handles the new (http://www.weblyzard.com/wl/2013#) weblyzard
XML format.

Functions added:
 - support for sentence tokens and pos iterators

Remove functions:
 - compatibility fixes for namespaces, encodings etc.
 - support for the old POS tags mapping.
'''
from __future__ import unicode_literals
from builtins import str
from builtins import object
import json

from weblyzard_api.model.parsers.xml_deprecated import XMLDeprecated
from weblyzard_api.model.parsers.xml_2005 import XML2005
from weblyzard_api.model.parsers.xml_2013 import XML2013
from weblyzard_api.model.parsers import EmptySentenceException
from weblyzard_api.model import Sentence, Annotation

SENTENCE_ATTRIBUTES = ('pos_tags', 'sem_orient', 'significance', 'md5sum',
                       'pos', 'token', 'dependency')


class XMLContent(object):

    SUPPORTED_XML_VERSIONS = {XML2005.VERSION: XML2005,
                              XML2013.VERSION: XML2013,
                              XMLDeprecated.VERSION: XMLDeprecated}
    API_MAPPINGS = {
        1.0: {
            'language_id': 'language_id',
            'lang': 'language_id',
            'xml:lang': 'language_id',
            'title': 'title',
            'uri': 'uri'
        }
    }

    ATTRIBUTE_MAPPING = {'uri': 'uri',
                         'content_id': 'id',
                         'title': 'title',
                         'sentences': 'sentences',
                         'body_annotations': 'annotations',
                         'lang': 'xml:lang',
                         'language_id': 'xml:lang',
                         'sentences_map': {'pos': 'pos',
                                           'token': 'token',
                                           'value': 'value',
                                           'md5sum': 'id'},
                         'annotations_map': {'start': 'start',
                                             'end': 'end',
                                             'key': 'key',
                                             'surfaceForm': 'surfaceForm'
                                             }}

    def __init__(self, xml_content, remove_duplicates=True):
        self.xml_version = None
        self.attributes = {}
        self.sentence_objects = []
        self.titles = []
        self.remove_duplicates = remove_duplicates

        self.body_annotations = []
        self.title_annotations = []
        self.features = {}
        self.relations = {}

        result = self.parse_xml_content(xml_content, remove_duplicates)

        if result:
            self.xml_version, self.attributes, self.sentence_objects, \
                self.title_annotations, self.body_annotations, self.titles, \
                self.features, self.relations = result
        pass

    @classmethod
    def convert(cls, xml_content, target_version):
        xml = XMLContent(xml_content)
        return xml.get_xml_document(xml_version=target_version)

    @classmethod
    def parse_xml_content(cls, xml_content, remove_duplicates=True):
        xml_version = cls.get_xml_version(xml_content)

        if not xml_version or not xml_content:
            return None

        sentence_objects = []
        annotation_objects = []
        parser = cls.SUPPORTED_XML_VERSIONS[xml_version]
        try:
            attributes, sentences, title_annotations, body_annotations, features, \
                relations = parser.parse(xml_content, remove_duplicates, raise_on_empty=True)
        except EmptySentenceException as e:
            raise EmptySentenceException('Empty sentence object: {}'.format(
                xml_content
            ))
        titles = []
        for sentence in sentences:
            try:
                sent_obj = Sentence(**sentence)
            except:
                sent_obj = Sentence(**{k:v for k,v in sentence.items() if k in Sentence.API_MAPPINGS[1.0]})

            if sent_obj.is_title:
                titles.append(sent_obj)
            else:
                sentence_objects.append(sent_obj)

        if len(titles) == 0 and 'title' in attributes:
            # fall back titles from attributes
            titles = [Sentence(value=attributes['title'], is_title=True)]

        for annotation in body_annotations:
            annotation_obj = Annotation(**annotation)
            annotation_objects.append(annotation_obj)
        return xml_version, attributes, sentence_objects, title_annotations, \
            annotation_objects, titles, features, relations

    @classmethod
    def get_xml_version(cls, xml_content):
        if not xml_content:
            return None

        for version, xml_parser in cls.SUPPORTED_XML_VERSIONS.items():
            if xml_parser.is_supported(xml_content):
                return version

    def get_xml_document(self, header_fields='all',
                         sentence_attributes=SENTENCE_ATTRIBUTES,
                         annotations=None,
                         features=None,
                         relations=None,
                         ignore_title=False,
                         xml_version=XML2013.VERSION):
        '''
        :param header_fields: the header_fields to include
        :param sentence_attributes: sentence attributes to include
        :param annotations, optionally
        :param features, optionally to overwrite
        :param relations, optionally to overwrite
        :param xml_version: version of the webLyzard XML format to use (XML2005.VERSION, *XML2013.VERSION*)
        :returns: the XML representation of the webLyzard XML object
        '''

        if not xml_version:
            xml_version = self.xml_version

        if not hasattr(self, 'features'):
            self.features = {}
        if features is None:
            features = self.features

        if not hasattr(self, 'relations'):
            self.relations = {}
        if relations is None:
            relations = self.relations

        titles = self.titles
        if ignore_title:
            titles = []

        return self.SUPPORTED_XML_VERSIONS[xml_version].dump_xml(titles=titles,
                                                                 attributes=self.attributes,
                                                                 sentences=self.sentences,
                                                                 annotations=annotations,
                                                                 features=features,
                                                                 relations=relations)

    def get_plain_text(self, include_title=False):
        ''' :returns: the plain text of the XML content '''
        if not len(self.all_sentences):
            return ''
        if not include_title:
            return '\n'.join([s.value for s in self.all_sentences if not s.is_title])
        else:
            return '\n'.join([s.value for s in self.all_sentences])

    @classmethod
    def get_text(cls, text):
        ''' :returns: the utf-8 encoded text '''
        if isinstance(text, str):
            text = text.decode('utf-8')
        return text

    def add_attribute(self, key, value):
        if not self.attributes:
            self.attributes = {}
        self.attributes[key] = value

    def update_attributes(self, new_attributes):
        '''
        Updates the existing attributes with new ones 

        :param new_attributes: The new attributes to set.
        :type new_attributes: dict
        '''

        # not using dict.update to allow advanced processing

        if not new_attributes or not isinstance(new_attributes, dict):
            return

        for k, v in new_attributes.items():
            self.attributes[str(k)] = v

    def update_features(self, new_features):
        if not new_features or not isinstance(new_features, dict):
            return

        for k, v in new_features.items():
            self.features[str(k)] = v

    def update_relations(self, new_relations):
        if not new_relations or not isinstance(new_relations, dict):
            return

        for k, v in new_relations.items():
            self.relations[str(k)] = v

    def as_dict(self, mapping=None, ignore_non_sentence=False,
                ignore_features=False, ignore_relations=False,
                add_titles_to_sentences=False):
        ''' convert the XML content to a dictionary.

        :param mapping: an optional mapping by which to restrict/rename \
            the returned dictionary
        :param ignore_non_sentence: if true, sentences without without POS tags \
            are omitted from the result
        :param ignore_features: if true, document features do not get serialized
        :param ignore_relations: if true, document relations do not get serialized
        :param add_titles_to_sentences: if true, titles are treated as sentences
        '''
        try:
            if mapping is None:
                mapping = self.ATTRIBUTE_MAPPING

            result = self.apply_dict_mapping(self.attributes, mapping)
            sentence_attr_name = mapping['sentences'] if 'sentences' in mapping else 'sentences'

            if 'sentences_map' in mapping:
                result[sentence_attr_name] = []
                sent_mapping = mapping['sentences_map']

                if add_titles_to_sentences and len(self.titles):
                    sentences = self.titles + self.sentences
                else:
                    sentences = self.sentences

                for sent in sentences:

                    if ignore_non_sentence and not sent.pos:
                        continue

                    sent_attributes = self.apply_dict_mapping(sent.as_dict(),
                                                              sent_mapping)
                    result[sentence_attr_name].append(sent_attributes)

            annotation_attr_name = mapping['body_annotations'] \
                if 'body_annotations' in mapping else 'body_annotations'
            if 'annotations_map' in mapping:
                result[annotation_attr_name] = []
                annotation_mapping = mapping['annotations_map']
                for annotation in self.body_annotations:
                    annotation_attributes = self.apply_dict_mapping(annotation.as_dict(),
                                                                    annotation_mapping)
                    result[annotation_attr_name].append(annotation_attributes)

            if not ignore_features and self.features:
                result['features'] = self.features

            if not ignore_relations and self.relations:
                result['relations'] = self.relations

        except Exception as e:
            result = self.attributes
            result.update({'sentences': [sent.as_dict()
                                         for sent in self.sentences]})

        return result

    @classmethod
    def apply_dict_mapping(cls, attributes, mapping=None):
        result = attributes

        if mapping:
            result = {}
            for attr, value in attributes.items():
                if attr in mapping:
                    result[mapping[attr]] = value

        return result

    def to_api_dict(self, version=1.0):
        '''
        Transforms the XMLContent object to a dict analoguous to the
        API JSON definition in the given version.

        :param version: The version to conform to.
        :type version: float
        :returns: A dict.
        :rtype: dict
        '''
        document_dict = self.as_dict()
        api_dict = {}
        for key in self.API_MAPPINGS[version]:
            if key in document_dict:
                api_dict[self.API_MAPPINGS[version][key]] = \
                    document_dict[key]
        if self.sentences and len(self.sentences) > 0:
            sentences = [s.to_api_dict(version) for s in self.sentences]
            api_dict['sentences'] = sentences
        if self.titles and len(self.titles) > 0:
            for t in self.titles:
                api_dict['sentences'] = [t.to_api_dict(
                    version)] + api_dict.get('sentences', [])
                if 'title' not in api_dict:
                    api_dict['title'] = t.value
#                 elif api_dict['title'] != t.value:
#                     raise Exception('Mismatch between sentence marked as title and '+\
#                                     'title attribute:\n'+\
#                                     '%s != %s' % (t.value, api_dict['title']))
        annotations = document_dict.get('annotations', None)
        if annotations:
            api_dict['annotations'] = annotations

        if self.features and len(self.features) > 0:
            api_dict['features'] = self.features
        if self.relations and len(self.relations) > 0:
            api_dict['relations'] = self.relations
        return api_dict

    def to_json(self, version=1.0):
        '''
        Serializes the XMLContent object to JSON according to the
        specified version.

        :param version: The version to conform to.
        :type version: float
        :returns: A JSON string.
        :rtype: str
        '''
        return json.dumps(self.to_api_dict(version=version))

    def _get_attribute(self, attr_name):
        ''' ::returns: the attribute for the given name '''
        return self.attributes.get(attr_name, None)

    def get_nilsimsa(self):
        return self._get_attribute('nilsimsa')

    def get_content_type(self):
        return self._get_attribute('content_type')

    def get_title(self):
        return self._get_attribute('title')

    def get_lang(self):
        if self._get_attribute('language_id') is not None:
            return self._get_attribute('language_id')
        return self._get_attribute('lang')

    def get_content_id(self):
        content_id = self._get_attribute('content_id')
        return int(content_id) if content_id else content_id

    def get_sentences(self, include_title_sentences=False):
        return self.titles * include_title_sentences + \
               self.sentence_objects

    def get_all_sentences(self):
        return self.get_sentences(include_title_sentences=True)

    def update_sentences(self, sentences):
        ''' 
        updates the values of the existing sentences. if the list of 
        sentence object is empty, sentence_objects will be set to the new
        sentences. 

        :param sentences: list of Sentence objects 

        .. warning:: this function will not add new sentences
        '''
        if not self.sentence_objects:
            self.sentence_objects = sentences
        else:
            sentence_dict = dict((sent.md5sum, sent) for sent in sentences)

            for sentence in self.sentence_objects:
                if sentence.md5sum in sentence_dict:
                    new_sentence = sentence_dict[sentence.md5sum]
                    for attrib in SENTENCE_ATTRIBUTES:
                        new_value = getattr(new_sentence, attrib)
                        if new_value:
                            setattr(sentence, attrib, new_value)

    all_sentences = property(get_all_sentences, update_sentences)
    sentences = property(get_sentences, update_sentences)
    plain_text = property(get_plain_text)
    nilsimsa = property(get_nilsimsa)
    content_type = property(get_content_type)
    title = property(get_title)
    lang = property(get_lang)
    content_id = property(get_content_id)
