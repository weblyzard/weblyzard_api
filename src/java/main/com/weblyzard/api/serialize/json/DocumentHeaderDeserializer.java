package com.weblyzard.api.serialize.json;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.DeserializationContext;
import com.fasterxml.jackson.databind.KeyDeserializer;
import com.weblyzard.api.model.document.Document;
import java.io.IOException;
import javax.xml.namespace.QName;

/**
 * Custom Map Key Serializer and Deserializer for header field in {@link Document} model class
 *
 * <p>The header field in the Document has QName objects as keys
 *
 * @author Norman Suesstrunk
 */
public class DocumentHeaderDeserializer extends KeyDeserializer {

    @Override
    public Object deserializeKey(String key, DeserializationContext ctxt)
            throws IOException, JsonProcessingException {
        return QName.valueOf(key);
    }
}
