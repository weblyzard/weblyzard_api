package com.weblyzard.api.serialize;

import java.util.Optional;
import com.weblyzard.api.model.Region;
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
    wl("http://www.weblyzard.com/wl/2013#"),
    dc("http://purl.org/dc/elements/1.1/"),
    xml("http://www.w3.org/XML/1998/namespace"),
    xsd("http://www.w3.org/2001/XMLSchema"),
    sioc("http://rdfs.org/sioc/ns#"),
    skos("http://www.w3.org/2004/02/skos/core#"),
    foaf("http://xmlns.com/foaf/0.1/"),
    ma("http://www.w3.org/ns/ma-ont#"),
    po("http://purl.org/ontology/po/"),
    rdf("http://www.w3.org/1999/02/22-rdf-syntax-ns#"),
    rdfs("http://www.w3.org/2000/01/rdf-schema#"),
    schema("http://schema.org/");
    //@formatter:on


    @Getter
    private final String namespace;

    private Namespace(String namespace) {
        this.namespace = namespace;
    }

    /**
     * Transforms a String into the corresponding {@link Region}.
     * 
     * @param region region String to be converted into an enum.
     * @return the Region constant for the given region (case insensitive)
     */
    public static Optional<Namespace> getNamespace(String prefix) {
        try {
            return Optional.of(valueOf(prefix.toLowerCase()));
        } catch (NullPointerException | IllegalArgumentException e) {
            return Optional.empty();
        }
    }
}
