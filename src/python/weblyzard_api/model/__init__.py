#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on May 14, 2018

.. codeauthor: Max Göbel <goebel@weblyzard.com>
'''
from __future__ import print_function
from __future__ import unicode_literals
from builtins import map
from builtins import str
from builtins import object
import json
import hashlib
import logging

from collections import namedtuple
from weblyzard_api.model.parsers.xml_2005 import XML2005
from weblyzard_api.model.parsers.xml_2013 import XML2013
from weblyzard_api.model.parsers.xml_deprecated import XMLDeprecated

LabeledDependency = namedtuple("LabeledDependency", "parent pos label")

logger = logging.getLogger(__name__)


class CharSpan(object):
    DICT_MAPPING = {'@type': 'span_type',
                    'start': 'start',
                    'end': 'end'}

    def __init__(self, span_type, start, end):
        self.span_type = span_type
        self.start = start
        self.end = end

    def to_dict(self):
        return {k: getattr(self, v) for k, v in self.DICT_MAPPING.items()}

    @classmethod
    def from_dict(cls, dict_):
        mismatched_keys = {k: v for k, v in dict_.items() if
                           k not in cls.DICT_MAPPING}
        if mismatched_keys:
            pass  # debugging
        kwargs = {cls.DICT_MAPPING[k]: v for k, v in dict_.items()}
        try:
            return cls(**kwargs)
        except TypeError as e:
            raise e

    def to_tuple(self):
        return (self.start, self.end)

    def __repr__(self, *args, **kwargs):
        return json.dumps(self.to_dict())


class TokenCharSpan(CharSpan):
    DICT_MAPPING = {'@type': 'span_type',
                    'start': 'start',
                    'end': 'end',
                    'pos': 'pos',
                    'dependency': 'dependency'}
    DEFAULT_POS = 'XY'

    def __init__(self, span_type, start, end, pos=None, dependency=None):
        CharSpan.__init__(self, span_type, start, end)
        if pos is None:
            pos = self.DEFAULT_POS
        self.pos = pos
        self.dependency = dependency

    # def to_dict(self):
    #     return {'@type': self.span_type,
    #             'start': self.start,
    #             'end': self.end,
    #             'pos': self.pos,
    #             'dependency': self.dependency}

    def __repr__(self, *args, **kwargs):
        return json.dumps(self.to_dict())


class SentenceCharSpan(CharSpan):
    DICT_MAPPING = {'@type': 'span_type',
                    'start': 'start',
                    'end': 'end',
                    'md5sum': 'md5sum',
                    'semOrient': 'sem_orient',
                    'significance': 'significance',
                    'id': 'md5sum'}

    def __init__(self, span_type, start, end, md5sum, sem_orient,
                 significance):
        CharSpan.__init__(self, span_type, start, end)
        self.md5sum = md5sum
        self.sem_orient = sem_orient
        self.significance = significance

    def __repr__(self, *args, **kwargs):
        return json.dumps(self.to_dict())


class NegationCharSpan(CharSpan):

    def __init__(self, span_type, start, end, value=None):
        super(NegationCharSpan, self).__init__(span_type=span_type, start=start,
                                               end=end)


class SentimentCharSpan(CharSpan):
    DICT_MAPPING = {'@type': 'span_type',
                    'start': 'start',
                    'end': 'end',
                    'value': 'value'}

    def __init__(self, span_type, start, end, value, **kwargs):
        super(SentimentCharSpan, self).__init__(span_type=span_type,
                                                start=start, end=end)
        self.value = value


class SpanFactory(object):
    SPAN_TYPE_TO_CLASS = {
        'CharSpan': CharSpan,
        'TokenCharSpan': TokenCharSpan,
        'SentimentCharSpan': SentimentCharSpan,
        'NegationCharSpan': NegationCharSpan,
        'SentenceCharSpan': SentimentCharSpan
    }

    @classmethod
    def new_span(cls, span):
        if span['span_type'] == 'SentenceCharSpan':
            return SentenceCharSpan(span_type='SentenceCharSpan',
                                    start=span['start'],
                                    end=span['end'],
                                    sem_orient=span.get('sem_orient', None),
                                    md5sum=span.get('md5sum', span.get('id')),
                                    significance=span.get('significance', None))
        elif span['span_type'] in cls.SPAN_TYPE_TO_CLASS:
            try:
                return cls.SPAN_TYPE_TO_CLASS[span['span_type']](**span)
            except Exception as e:
                logger.warning(
                    "Unable to process  span {}. Error was {}".format(span, e),
                    exc_info=True)
                raise e
        raise Exception('Invalid Span Type: {}'.format(span['span_type']))


class Annotation(object):

    def __init__(self, annotation_type=None, start=None, end=None, key=None,
                 sentence=None, surfaceForm=None, md5sum=None, sem_orient=None,
                 preferredName=None, confidence=None):
        self.annotation_type = annotation_type
        self.surfaceForm = surfaceForm
        self.start = start
        self.end = end
        self.key = key
        self.sentence = sentence
        self.md5sum = md5sum
        self.sem_orient = sem_orient
        self.preferredName = preferredName
        self.confidence = confidence


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

    # Delimiter between items (POS, TOKEN, DEPENDENCY)
    ITEM_DELIMITER = ' '

    # Delimiter for a single token
    TOKEN_DELIMITER = ','

    # Delimiter for a single dependency
    DEPENDENCY_DELIMITER = ':'

    def __init__(self, md5sum=None, pos=None, sem_orient=None,
                 significance=None,
                 token=None, value=None, is_title=False, dependency=None):

        if not md5sum and value:
            try:
                m = hashlib.md5()
                m.update(value.encode('utf-8')
                         if isinstance(value, str) else str(value).encode(
                    'utf-8'))
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
        return dict((k, v) for k, v in self.__dict__.items() if
                    not k.startswith('_'))

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
            return self.pos.strip().split(self.ITEM_DELIMITER)
        else:
            return None

    def set_pos_tags(self, new_pos_tags):
        if isinstance(new_pos_tags, list):
            new_pos_tags = self.ITEM_DELIMITER.join(new_pos_tags)
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
        correction_offset = int(self.token.split(',')[0] or 0)
        for token_pos in self.token.split(self.ITEM_DELIMITER):
            token_indices = token_pos.split(self.TOKEN_DELIMITER)
            try:
                start, end = [int(i) - correction_offset for i \
                              in token_indices]
            except ValueError as e:
                # occasionally there appear to be missing spaces in token
                # strings
                logger.warn('Error parsing tokens for sentence {}; token '
                            'string was {}; individual token identifier '
                            'was {}. Original error was: {}'.format(
                    self.value, self.token, token_pos, e
                ), exc_info=True)
                token_indices = [int(tok) for tok in token_indices]
                start, end = token_indices[0], token_indices[-1]
            res = str(self.sentence)[start:end]
            # de- and encoding sometimes leads to index errors with double-width
            # characters - here we attempt to detect such cases and correct
            if res.strip() != res:
                correction_offset += len(res) - len(res.strip())
                res = res.strip()
            yield res

    def is_digit(self, x):
        """built in is_digit rejects negative number strings like -1 (used for
        root in dependency annotations"""
        try:
            _ = int(x)
            return True
        except ValueError:
            return False

    def get_dependency_list(self):
        '''
        :returns: the dependencies of the sentence as a list of \
            `LabeledDependency` objects
        :rtype: :py:class:`list` of :py:class:\
            `weblyzard_api.model.xml_content.LabeledDependency` objects

        >>> s = Sentence(pos='RB PRP MD', dependency='1:SUB -1:ROOT 1:OBJ')
        >>> s.dependency_list
        [
        LabeledDependency(parent='1', pos='RB', label='SUB'),
        LabeledDependency(parent='-1', pos='PRP', label='ROOT'),
        LabeledDependency(parent='1', pos='MD', label='OBJ')
        ]
        '''
        if self.dependency:
            result = []
            deps = self.dependency.strip().split(self.ITEM_DELIMITER)
            for index, dep in enumerate(deps):
                if self.DEPENDENCY_DELIMITER in dep:

                    parent, label = dep.split(self.DEPENDENCY_DELIMITER, 1)
                    if not self.is_digit(parent):
                        try:
                            label, parent = parent, label
                            assert self.is_digit(parent)
                        except AssertionError:
                            logger.info(
                                'Unable to parse dependeny annotation {} for sentence '
                                '{} with dependency string {} as tuple of '
                                '(parent index, dependency label), treating it as '
                                'parent index only'.format(dep, self.value,
                                                           self.dependency))
                            parent, label = -1, 'XX'
                elif self.is_digit(dep):
                    parent, label = dep, None
                    logger.info(
                        'Unable to parse dependeny annotation {} for sentence '
                        '{} with dependency string {} as tuple of '
                        '(parent index, dependency label), treating it as '
                        'parent index only'.format(dep, self.value,
                                                   self.dependency))
                else:
                    parent, dep = -1, dep
                    logger.info(
                        'Unable to parse dependeny annotation {} for sente'
                        'nce '
                        '{} with dependency string {} as tuple of '
                        '(parent index, dependency label), treating it as '
                        'dependency label only'.format(dep, self.value,
                                                       self.dependency))
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
        [LabeledDependency(parent='1', pos='RB', label='SUB'),
        LabeledDependency(parent='-1', pos='PRP', label='ROOT'),
        LabeledDependency(parent='1', pos='MD', label='OBJ')]
        >>> s.dependency_list = [LabeledDependency(parent='-1', pos='MD', label='ROOT'), ]
        >>> s.dependency_list
        [LabeledDependency(parent='-1', pos='MD', label='ROOT')]
        '''
        if not dependencies:
            return
        deps = []
        new_pos = []
        for dependency in dependencies:
            deps.append(self.DEPENDENCY_DELIMITER.join(
                [dependency.parent, dependency.label]))
            new_pos.append(dependency.pos)
        self.pos = self.ITEM_DELIMITER.join(new_pos)
        self.dependency = self.ITEM_DELIMITER.join(deps)

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
                self.as_dict().items() if key in key_map and
                value is not None}

    sentence = property(get_sentence, set_sentence)
    pos_tags = property(get_pos_tags, set_pos_tags)
    tokens = property(get_tokens)
    pos_tags_list = property(get_pos_tags_list, set_pos_tags_list)
    pos_tag_string = property(get_pos_tags_string, set_pos_tags_string)
    dependency_list = property(get_dependency_list, set_dependency_list)
