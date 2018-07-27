package com.weblyzard.api.serialize.json;

import java.io.IOException;
import com.fasterxml.jackson.core.JsonParser;
import com.fasterxml.jackson.databind.DeserializationContext;
import com.fasterxml.jackson.databind.deser.std.StdDeserializer;
import com.weblyzard.api.datatype.MD5Digest;

public class MD5DigestDeserializer extends StdDeserializer<MD5Digest> {

    private static final long serialVersionUID = 1L;

    public MD5DigestDeserializer() {
        this(null);
    }

    protected MD5DigestDeserializer(Class<?> vc) {
        super(vc);
    }

    @Override
    public MD5Digest deserialize(JsonParser p, DeserializationContext ctxt) throws IOException {
        return MD5Digest.fromHexDigest(p.getValueAsString());
    }
}
