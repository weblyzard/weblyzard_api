#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on May 14, 2018

.. codeauthor: Max Göbel <goebel@weblyzard.com>
'''
import json
import hashlib

from collections import namedtuple
from weblyzard_api.model.parsers.xml_2005 import XML2005
from weblyzard_api.model.parsers.xml_2013 import XML2013
from weblyzard_api.model.parsers.xml_deprecated import XMLDeprecated

LabeledDependency = namedtuple("LabeledDependency", "parent pos label")


class SpanFactory(object):

    @classmethod
    def new_span(cls, span):
        assert isinstance(span, dict) and '@type' in span

        if span['@type'] == 'CharSpan':
            return CharSpan(span_type='CharSpan', start=span['start'], end=span['end'])
        elif span['@type'] == 'TokenCharSpan':
            return TokenCharSpan(span_type='TokenCharSpan', start=span['start'],
                                 end=span['end'], pos=span['pos'],
                                 dependency=span['dependency'])
        elif span['@type'] == 'SentenceCharSpan':
            return SentenceCharSpan(span_type='SentenceCharSpan', start=span['start'],
                                    end=span['end'], sem_orient=span['sem_orient'],
                                    md5sum=span['id'], significance=span['significance'])
        raise Exception('Invalid Span Type: {}'.format(span['@type']))


class CharSpan(object):

    def __init__(self, span_type, start, end):
        self.span_type = span_type
        self.start = start
        self.end = end


class TokenCharSpan(CharSpan):

    def __init__(self, span_type, start, end, pos, dependency=None):
        CharSpan.__init__(self, span_type, start, end)
        self.pos = pos
        self.dependency = dependency


class SentenceCharSpan(CharSpan):

    def __init__(self, span_type, start, end, md5sum, sem_orient,
                 significance):
        CharSpan.__init__(self, span_type, start, end)
        self.md5sum = md5sum
        self.sem_orient = sem_orient
        self.significance = significance


class Annotation(object):

    def __init__(self, annotation_type=None, start=None, end=None, key=None,
                 sentence=None, surfaceForm=None, md5sum=None, sem_orient=None,
                 preferredName=None):
        self.annotation_type = annotation_type
        self.surfaceForm = surfaceForm
        self.start = start
        self.end = end
        self.key = key
        self.sentence = sentence
        self.md5sum = md5sum
        self.sem_orient = sem_orient
        self.preferredName = preferredName


class Sentence(object):
    '''
    The sentence class used for accessing single sentences.

    .. note::

        the class provides convenient properties for accessing pos tags and tokens:

        * s.sentence: sentence text
        * s.tokens  : provides a list of tokens (e.g. ['A', 'new', 'day'])
        * s.pos_tags: provides a list of pos tags (e.g. ['DET', 'CC', 'NN'])
    '''
    #:  Maps the keys of the attributes to the corresponding key for the API JSON
    API_MAPPINGS = {
        1.0: {
            'md5sum': 'id',
            'value': 'value',
            'pos': 'pos_list',
            'sem_orient': 'polarity',
            'token': 'tok_list',
            'is_title': 'is_title',
            'dependency': 'dep_tree',
        }
    }

    def __init__(self, md5sum=None, pos=None, sem_orient=None, significance=None,
                 token=None, value=None, is_title=False, dependency=None):

        if not md5sum and value:
            try:
                m = hashlib.md5()
                m.update(value.encode('utf-8')
                         if isinstance(value, unicode) else str(value))
                md5sum = m.hexdigest()
            except Exception as e:
                print(e)

        self.md5sum = md5sum
        self.pos = pos
        self.sem_orient = sem_orient
        self.significance = significance
        self.token = token
        self.value = value
        self.is_title = is_title
        self.dependency = dependency

    def as_dict(self):
        '''
        :returns: a dictionary representation of the sentence object.
        '''
        return dict((k, v) for k, v in self.__dict__.iteritems() if not k.startswith('_'))

    def get_sentence(self):
        return self.value

    def set_sentence(self, new_sentence):
        self.value = new_sentence

    def get_pos_tags(self):
        '''
        Get the POS Tags as list.

        >>> sentence = Sentence(pos = 'PRP ADV NN')
        >>> sentence.get_pos_tags()
        ['PRP', 'ADV', 'NN']
        '''
        if self.pos:
            return self.pos.strip().split()
        else:
            return None

    def set_pos_tags(self, new_pos_tags):
        if isinstance(new_pos_tags, list):
            new_pos_tags = ' '.join(new_pos_tags)
        self.pos = new_pos_tags

    def get_pos_tags_list(self):
        '''
        :returns: list of the sentence's POS tags

        >>> sentence = Sentence(pos = 'PRP ADV NN')
        >>> sentence.get_pos_tags_list()
        ['PRP', 'ADV', 'NN']
        '''
        return [] if not self.pos_tag_string else self.get_pos_tags()

    def set_pos_tags_list(self, pos_tags_list):
        self.set_pos_tags(pos_tags_list)

    def get_pos_tags_string(self):
        '''
        :returns: String of the sentence's POS tags

        >>> sentence = Sentence(pos = 'PRP ADV NN')
        >>> sentence.get_pos_tags_string()
        'PRP ADV NN'
        '''
        return self.pos

    def set_pos_tags_string(self, new_value):
        self.pos = new_value

    def get_tokens(self):
        '''
        :returns: an iterator providing the sentence's tokens 
        '''
        if not self.token:
            raise StopIteration

        for token_pos in self.token.split(' '):
            start, end = map(int, token_pos.split(','))
            # yield self.sentence.decode('utf8')[start:end]
            yield unicode(self.sentence)[start:end]

    def get_dependency_list(self):
        '''
        :returns: the dependencies of the sentence as a list of \
            `LabeledDependency` objects
        :rtype: :py:class:`list` of :py:class:\
            `weblyzard_api.model.xml_content.LabeledDependency` objects

        >>> s = Sentence(pos='RB PRP MD', dependency='1:SUB -1:ROOT 1:OBJ')
        >>> s.dependency_list
        [LabeledDependency(parent='1', pos='RB', label='SUB'), LabeledDependency(parent='-1', pos='PRP', label='ROOT'), LabeledDependency(parent='1', pos='MD', label='OBJ')]
        '''
        if self.dependency:
            result = []
            deps = self.dependency.strip().split(' ')
            for index, dep in enumerate(deps):
                [parent, label] = dep.split(':') if ':' in dep else [dep, None]
                result.append(LabeledDependency(parent,
                                                self.pos_tags_list[index],
                                                label))
            return result
        else:
            return None

    def set_dependency_list(self, dependencies):
        '''
        Takes a list of :py:class:`weblyzard_api.model.xml_content.LabeledDependency`

        :param dependencies: The dependencies to set for this sentence.
        :type dependencies: list

        .. note:: The list must contain items of the type \
            :py:class:`weblyzard_api.model.xml_content.LabeledDependency`

        >>> s = Sentence(pos='RB PRP MD', dependency='1:SUB -1:ROOT 1:OBJ')
        >>> s.dependency_list
        [LabeledDependency(parent='1', pos='RB', label='SUB'), LabeledDependency(parent='-1', pos='PRP', label='ROOT'), LabeledDependency(parent='1', pos='MD', label='OBJ')]
        >>> s.dependency_list = [LabeledDependency(parent='-1', pos='MD', label='ROOT'), ]
        >>> s.dependency_list
        [LabeledDependency(parent='-1', pos='MD', label='ROOT')]
        '''
        if not dependencies:
            return
        deps = []
        new_pos = []
        for dependency in dependencies:
            deps.append(dependency.parent + ':' + dependency.label)
            new_pos.append(dependency.pos)
        self.pos = ' '.join(new_pos)
        self.dependency = ' '.join(deps)

    def to_json(self, version=1.0):
        '''
        Converts the Sentence object to the corresponding JSON string
        according to the given API version (default 1.0).

        :param version: The API version to target.
        :type version: float
        :returns: A JSON string.
        :rtype: str
        '''
        return json.dumps(self.to_api_dict(version))

    def to_api_dict(self, version=1.0):
        '''
        Serializes the Sentence object to a dict conforming to the
        specified API version (default 1.0).

        :param version: The API version to target.
        :type version: float
        :returns: A dict with the correct keys as defined in the API.
        :rtype: dict
        '''
        key_map = self.API_MAPPINGS[version]
        return {key_map[key]: value for key, value in
                self.as_dict().iteritems() if key in key_map and
                value is not None}

    sentence = property(get_sentence, set_sentence)
    pos_tags = property(get_pos_tags, set_pos_tags)
    tokens = property(get_tokens)
    pos_tags_list = property(get_pos_tags_list, set_pos_tags_list)
    pos_tag_string = property(get_pos_tags_string, set_pos_tags_string)
    dependency_list = property(get_dependency_list, set_dependency_list)
