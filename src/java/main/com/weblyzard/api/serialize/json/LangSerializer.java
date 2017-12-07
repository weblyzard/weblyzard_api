package com.weblyzard.api.serialize.json;

import java.io.IOException;
import com.fasterxml.jackson.core.JsonGenerator;
import com.fasterxml.jackson.databind.SerializerProvider;
import com.fasterxml.jackson.databind.ser.std.StdSerializer;
import com.weblyzard.api.model.Lang;

public class LangSerializer extends StdSerializer<Lang> {

    public LangSerializer() {
        this(null);
    }

    protected LangSerializer(Class<Lang> t) {
        super(t);
    }
    
    @Override
    public void serialize(Lang value, JsonGenerator generator, SerializerProvider provider)
            throws IOException {
        generator.writeString(value.toString());
    }
   
    private static final long serialVersionUID = 1L;
}
