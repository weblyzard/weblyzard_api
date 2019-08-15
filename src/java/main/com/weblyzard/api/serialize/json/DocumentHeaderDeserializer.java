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

        try {
            QName result = QName.valueOf(key);

            // check if we were able to parse the QName into namespace and localpart:
            if (result.getNamespaceURI().length() == 0) {
                throw new InvalidPropertiesFormatException(String.format(
                        "could not deserialize key %s. Expected format is '{namespace}localpart'",
                        key));
            }

            return result;

        } catch (IllegalArgumentException e) {
            // catch any presence of IAE that could potentially be risen by `QName.valueOf`
            throw new InvalidPropertiesFormatException(String
                    .format("parsing qname %s raised an IllegalArgumentException: %s", key, e));
        }
    }
}
