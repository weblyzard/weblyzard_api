package com.weblyzard.api.serialize.json;

import com.fasterxml.jackson.core.JsonGenerationException;
import com.fasterxml.jackson.core.JsonGenerator;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializerProvider;
import com.fasterxml.jackson.databind.ser.std.StdKeySerializer;
import com.weblyzard.api.model.document.Document;
import java.io.IOException;

/**
 * Custom Key Serializer for header field in {@link Document} model class
 *
 * <p>The header field in the Document has QName objects as keys
 *
 * @author Norman Suesstrunk
 */
public class DocumentHeaderSerializer extends StdKeySerializer {

    private static final long serialVersionUID = 1L;

    private ObjectMapper mapper = new ObjectMapper();

    @Override
    public void serialize(Object value, JsonGenerator jgen, SerializerProvider provider)
            throws IOException, JsonGenerationException {
        jgen.writeFieldName(mapper.writeValueAsString(value));
    }
}
