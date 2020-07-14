#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from enum import Enum


class Namespace(Enum):
    XML = 'http://www.w3.org/XML/1998/namespace'
    XSD = 'http://www.w3.org/2001/XMLSchema#'
    RDF = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
    RDFS = 'http://www.w3.org/2000/01/rdf-schema#'
    OWL = 'http://www.w3.org/2002/07/owl#'
    PROV = 'http://www.w3.org/ns/prov#'
    DC = 'http://purl.org/dc/elements/1.1/'
    DCT = 'http://purl.org/dc/terms/'
    SCHEMA = 'http://schema.org/'

    # special interest namespaces
    SKOS = 'http://www.w3.org/2004/02/skos/core#'
    FOAF = 'http://xmlns.com/foaf/0.1/'
    MA = 'http://www.w3.org/ns/ma-ont#'
    SIOC = 'http://rdfs.org/sioc/ns#'
    PO = 'http://purl.org/ontology/po/'

    # lexical namespaces
    LEMON = 'http://lemon-model.net/lemon#'
    LEXINFO = 'http://www.lexinfo.net/ontology/2.0/lexinfo#'
    LANG = 'http://id.loc.gov/vocabulary/iso639-1/'

    # wikidata, dbpedia, geo
    DBO = 'http://dbpedia.org/ontology/'
    GEO = 'http://www.opengis.net/ont/geosparql#'
    WDT = 'http://www.wikidata.org/prop/direct/'
    WD = 'http://www.wikidata.org/entity/'
    P = 'http://www.wikidata.org/prop/'
    PS = 'http://www.wikidata.org/prop/statement/'
    PQ = 'http://www.wikidata.org/prop/qualifier/'
    GEONAMES = 'http://sws.geonames.org/'
    GN = 'http://www.geonames.org/ontology#'
    OSM = 'http://www.openstreetmap.org/way/'

    # weblyzard namespaces
    WL = 'http://www.weblyzard.com/wl/2013#'
    SKBLEX = 'http://weblyzard.com/skb/lexicon/'
    SKBPROP = 'http://weblyzard.com/skb/property/'
    SKBENTITY = 'http://weblyzard.com/skb/entity/'
    SKBPERSON = 'http://weblyzard.com/skb/entity/person/'
    SKBORG = 'http://weblyzard.com/skb/entity/organization/'
    SKBGEO = 'http://weblyzard.com/skb/entity/geo/'
    SKBEVENT = 'http://weblyzard.com/skb/event/'
    SKBCAT = 'http://weblyzard.com/skb/entity/category/'
    AGENT = 'http://weblyzard.com/skb/entity/agent/'

    # weblyzard keywords per language
    SKBKWEN = 'http://weblyzard.com/skb/keyword/en#'
    SKBKWDE = 'http://weblyzard.com/skb/keyword/de#'
    SKBKWFR = 'http://weblyzard.com/skb/keyword/fr#'
    SKBKWES = 'http://weblyzard.com/skb/keyword/es#'
    SKBKWIT = 'http://weblyzard.com/skb/keyword/it#'
    SKBKWPT = 'http://weblyzard.com/skb/keyword/pt#'
    SKBKWZH = 'http://weblyzard.com/skb/keyword/zh#'
    SKBKWRU = 'http://weblyzard.com/skb/keyword/ru#'
    SKBKWAR = 'http://weblyzard.com/skb/keyword/ar#'
    SKBKWNL = 'http://weblyzard.com/skb/keyword/nl#'

    @classmethod
    def to_fully_qualified(cls, prefix: str) -> str:
        """ Look up short prefix and return fully-qualified URL if known.
        :param prefix: the prefix to be resolved.
        :returns the fully-qualified URL or the prefix if unknown.
        """
        prefix = prefix.upper()
        if hasattr(Namespace, prefix):
            return getattr(cls, prefix).value
        return prefix

    @classmethod
    def to_prefix(cls, uri: str) -> str:
        """ 
        """
        try:
            return Namespace(uri).name.lower()
        except Exception as e:
            pass


NAMESPACES = {item.value: item.name.lower() for item in Namespace}

PREFIXES = '\n'.join([''] + ['PREFIX {value}: <{key}>'.format(value=item.name.lower(),
                                                              key=item.value)
                             for item in Namespace])


def to_fully_qualified(attribute: str) -> str:
    """ QName originates from the XML world, where it is used to reduce I/O by shortening 
    namespaces (e.g. http://www.weblyzard.com/wl/2013#) to a prefix (e.g. wl) 
    followed by the local part (e.g. jonas_type). The namespace-prefix relations 
    are thereby defined in the XML-Head. This relation mapping does not exist in JSON, 
    which is why we have to have the full qualified name (namespace + local part) 
    to define an attribute. While the more readable way would be to just use the URI, 
    the official standardized format is {namespace}localpart, having the major 
    advantage of non-ambiguous namespace identification. Further, Java expects Qnames 
    in this annotation format, which enables to simply use Qname.valueOf(key).
    :param attribute: the attribute to resolve
    :returns a fully-qualified version of the input attribute.
    """
    if len(attribute.split(':')) <= 1 or attribute.startswith('{'):
        return attribute

    namespace, attr_name = attribute.split(':')
    return '{%s}%s' % (Namespace.to_fully_qualified(namespace), attr_name)


def prefix_uri(uri: str, allow_partial: bool=False) -> str:
    """ Replace a sub-path from the uri with the most specific prefix as defined
    in the Namespace.
    :param uri: The URI to modify.
    :type uri: str
    :param allow_partial: if True allow partial replacements
    :type allow_partial: bool
    :returns: The modified URI if applicable
    :rtype: str
    """
    if not uri.startswith('http'):
        return uri
    # replace most specific/longest prefix, hence sorted
    for namespace in sorted(list([ns.value for ns in Namespace]), key=len, reverse=True):
        if namespace in uri:
            replaced = uri.replace(
                namespace, '{}:'.format(Namespace.to_prefix(namespace)))
            if '/' in replaced[:-1] or '#' in replaced[:-1]:
                if not allow_partial:
                    # slashes or hashes in prefixed URIs only allowed at the
                    # end
                    continue
            return replaced
    return uri


def replace_prefix(uri):
    """ Replace a prefix with the fully-qualified namespace URL.
    :param uri: The URI to modify.
    :type uri: str
    :returns: The modified URI if applicable
    :rtype: str
    """
    for namespace in sorted(list(NAMESPACES.keys()), key=len, reverse=True):
        prefix = '{}:'.format(NAMESPACES[namespace])
        if uri.startswith(prefix):
            return uri.replace(prefix, namespace)
    return uri


def parse_language_tagged_string(value: str) -> tuple:
    """ Check if a string value has a language tag @xx or @xxx
    and returns the string without the value tag and language
    as tuple. If no language tag -> language is None
    :param value
    :returns:
    """
    lang = None
    if len(value) > 1 and value[0] == value[-1] == '"':
        value = value[1:-1]
    if len(value) > 6 and value[-6] == '@':
        lang = value[-5:]
        value = value[:-6]
    elif len(value) > 3 and value[-3] == '@':
        lang = value[-2:]
        value = value[:-3]
    elif len(value) > 4 and value[-4] == '@':
        lang = value[-3:]
        value = value[:-4]
    return value, lang
