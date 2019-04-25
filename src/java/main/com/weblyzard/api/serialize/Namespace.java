package com.weblyzard.api.serialize;

import java.util.Optional;
import lombok.Getter;

/**
 * Enum representation of <code>src/python/weblyzard_api/model/parsers/xml_2013.py</code>.
 * 
 * Used to parse known prefixes into their corresponding namespace.
 * 
 * @author Philipp.Kuntschik@htwchur.ch
 *
 */
public enum Namespace {

    //@formatter:off
    WL("wl", "http://www.weblyzard.com/wl/2013#"),
    DC("dc", "http://purl.org/dc/elements/1.1/"),
    XML("xml", "http://www.w3.org/xml/1998/namespace"),
    XSD("xsd", "http://www.w3.org/2001/xmlschema"),
    SIOC("sioc", "http://rdfs.org/sioc/ns#"),
    SKOS("skos", "http://www.w3.org/2004/02/skos/core#"),
    FOAF("foaf", "http://xmlns.com/foaf/0.1/"),
    MA("ma", "http://www.w3.org/ns/ma-ont#"),
    PO("po", "http://purl.org/ontology/po/"),
    RDF("rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#"),
    RDFS("rdfs", "http://www.w3.org/2000/01/rdf-schema#"),
    SCHEMA("schema", "http://schema.org/");
    //@formatter:on

    @Getter
    private final String prefix;

    @Getter
    private final String uri;


    private Namespace(String prefix, String uri) {
        this.prefix = prefix;
        this.uri = uri;
    }

    /**
     * Transforms a String into the corresponding {@link Namespace}.
     * 
     * @param prefix prefix String to be converted into an enum.
     * @return the Namespace constant for the given region (case insensitive)
     */
    public static Optional<Namespace> getNamespace(String prefix) {
        try {
            return Optional.of(valueOf(prefix.toUpperCase()));
        } catch (NullPointerException | IllegalArgumentException e) {
            return Optional.empty();
        }
    }
}
