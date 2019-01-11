package com.weblyzard.api.serialize.json;

import java.io.IOException;
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
    public Object deserializeKey(String key, DeserializationContext ctxt) throws IOException {
        return QName.valueOf(key);
    }
}
