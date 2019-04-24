package com.weblyzard.api.serialize.json;

import java.io.IOException;
import java.util.Arrays;
import java.util.Optional;
import javax.xml.namespace.QName;
import com.fasterxml.jackson.databind.DeserializationContext;
import com.fasterxml.jackson.databind.KeyDeserializer;
import com.weblyzard.api.model.document.LegacyDocument;
import com.weblyzard.api.serialize.Namespace;

/**
 * Custom Map Key Serializer and Deserializer for header field in {@link LegacyDocument} model
 * class.
 * <p>
 * The header field in the Document has QName objects as keys
 *
 * @author Norman Suesstrunk
 */
public class DocumentHeaderDeserializer extends KeyDeserializer {

    @Override
    public Object deserializeKey(String key, DeserializationContext ctxt) throws IOException {

        // check if key represents a supported full qualified URI
        Optional<Namespace> optionalNamespace = Arrays.stream(Namespace.values())
                .filter(namespace -> key.startsWith(namespace.getNamespace())).findFirst();

        if (optionalNamespace.isPresent()) {
            Namespace namespace = optionalNamespace.get();
            String local = key.substring(namespace.getNamespace().length());
            return new QName(namespace.getNamespace(), local, namespace.name());
        }

        // check if key represents a supported prefixed URI
        String[] parts = key.split(":");
        if (parts.length == 2) {
            String prefix = parts[0];
            String local = parts[1];
            Optional<Namespace> optionalPrefix = Namespace.getNamespace(prefix);

            if (optionalPrefix.isPresent()) {
                Namespace namespace = optionalPrefix.get();
                return new QName(namespace.getNamespace(), local, namespace.name());
            }
        }

        return QName.valueOf(key);
    }
}
