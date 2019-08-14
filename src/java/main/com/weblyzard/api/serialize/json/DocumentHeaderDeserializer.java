package com.weblyzard.api.serialize.json;

import java.util.InvalidPropertiesFormatException;
import javax.xml.namespace.QName;
import com.fasterxml.jackson.databind.DeserializationContext;
import com.fasterxml.jackson.databind.KeyDeserializer;
import com.weblyzard.api.model.document.LegacyDocument;

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
    public Object deserializeKey(String key, DeserializationContext ctxt)
            throws InvalidPropertiesFormatException {

        // check if the QName is represented according to specification
        if (key.startsWith("{")) {
            return QName.valueOf(key);
        }

        throw new InvalidPropertiesFormatException(String.format(
                "could not deserialize key %s. Expected format is '{namespace}localpart'", key));

    }
}
