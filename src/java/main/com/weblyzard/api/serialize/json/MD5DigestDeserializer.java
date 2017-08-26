package com.weblyzard.api.serialize.json;

import com.fasterxml.jackson.core.JsonParser;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.DeserializationContext;
import com.fasterxml.jackson.databind.deser.std.StdDeserializer;
import com.weblyzard.api.datatype.MD5Digest;
import java.io.IOException;

public class MD5DigestDeserializer extends StdDeserializer<MD5Digest> {

    private static final long serialVersionUID = 1L;

    public MD5DigestDeserializer() {
        this(null);
    }

    protected MD5DigestDeserializer(Class<?> vc) {
        super(vc);
    }

    @Override
    public MD5Digest deserialize(JsonParser p, DeserializationContext ctxt)
            throws IOException, JsonProcessingException {
        return MD5Digest.fromText(p.getValueAsString());
    }
}
