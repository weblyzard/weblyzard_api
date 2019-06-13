package com.weblyzard.api.serialize.json;

import java.io.IOException;
import java.util.AbstractMap;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Optional;
import javax.xml.namespace.QName;
import com.fasterxml.jackson.databind.DeserializationContext;
import com.fasterxml.jackson.databind.KeyDeserializer;
import com.weblyzard.api.model.document.LegacyDocument;

/**
 * Custom Map Key Serializer and Deserializer for header field in {@link LegacyDocument} model class.
 * <p>
 * The header field in the Document has QName objects as keys
 *
 * @author Norman Suesstrunk
 */
public class DocumentHeaderDeserializer extends KeyDeserializer {

    /**
     * map of all namespaces, supported and used in any weblyzard component, see
     * <code>src/python/weblyzard_api/model/parsers/xml_2013.py</code>.
     */
    //@formatter:off
    private static final Map<String, String> namespaces = Map.ofEntries(
        new AbstractMap.SimpleImmutableEntry<>("wl", "http://www.weblyzard.com/wl/2013#"),
        new AbstractMap.SimpleImmutableEntry<>("dc", "http://purl.org/dc/elements/1.1/"),
        new AbstractMap.SimpleImmutableEntry<>("xml", "http://www.w3.org/xml/1998/namespace"),
        new AbstractMap.SimpleImmutableEntry<>("xsd", "http://www.w3.org/2001/xmlschema"),
        new AbstractMap.SimpleImmutableEntry<>("sioc", "http://rdfs.org/sioc/ns#"),
        new AbstractMap.SimpleImmutableEntry<>("skos", "http://www.w3.org/2004/02/skos/core#"),
        new AbstractMap.SimpleImmutableEntry<>("foaf", "http://xmlns.com/foaf/0.1/"),
        new AbstractMap.SimpleImmutableEntry<>("ma", "http://www.w3.org/ns/ma-ont#"),
        new AbstractMap.SimpleImmutableEntry<>("po", "http://purl.org/ontology/po/"),
        new AbstractMap.SimpleImmutableEntry<>("rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#"),
        new AbstractMap.SimpleImmutableEntry<>("rdfs", "http://www.w3.org/2000/01/rdf-schema#"),
        new AbstractMap.SimpleImmutableEntry<>("schema", "http://schema.org/")
    );
    //@formatter:on


    @Override
    public Object deserializeKey(String key, DeserializationContext ctxt) throws IOException {

        // check if key represents a supported full qualified URI
        Optional<Entry<String, String>> optionalNamespace = namespaces.entrySet().stream()
                .filter(entry -> key.startsWith(entry.getValue())).findFirst();

        if (optionalNamespace.isPresent()) {
            Entry<String, String> namespace = optionalNamespace.get();
            String local = key.substring(namespace.getValue().length());
            return new QName(namespace.getValue(), local, namespace.getKey());
        }

        // check if key represents a supported prefixed URI
        String[] parts = key.split(":");
        if (parts.length == 2) {
            String prefix = parts[0];
            String local = parts[1];
            if (namespaces.containsKey(prefix)) {
                return new QName(namespaces.get(prefix), local, prefix);
            }
        }

        return QName.valueOf(key);
    }
}
