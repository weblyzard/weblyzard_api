package com.weblyzard.api.serialize.json;

import java.io.IOException;
import com.fasterxml.jackson.core.JsonGenerator;
import com.fasterxml.jackson.databind.SerializerProvider;
import com.fasterxml.jackson.databind.ser.std.StdSerializer;
import com.weblyzard.api.datatype.MD5Digest;

public class MD5DigestSerializer extends StdSerializer<MD5Digest> {

    private static final long serialVersionUID = 1L;

    public MD5DigestSerializer() {
        this(null);
    }

    protected MD5DigestSerializer(Class<MD5Digest> t) {
        super(t);
    }

    @Override
    public void serialize(MD5Digest value, JsonGenerator jgen, SerializerProvider provider) throws IOException {
        jgen.writeString(value.toString());
    }
}
