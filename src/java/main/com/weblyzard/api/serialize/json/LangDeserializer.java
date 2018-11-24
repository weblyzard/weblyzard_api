package com.weblyzard.api.serialize.json;

import java.io.IOException;
import com.fasterxml.jackson.core.JsonParser;
import com.fasterxml.jackson.databind.DeserializationContext;
import com.fasterxml.jackson.databind.deser.std.StdDeserializer;
import com.weblyzard.api.model.Lang;

public class LangDeserializer extends StdDeserializer<Lang> {

    private static final long serialVersionUID = 1L;

    public LangDeserializer() {
        this(null);
    }

    protected LangDeserializer(Class<?> vc) {
        super(vc);
    }

    @Override
    public Lang deserialize(JsonParser p, DeserializationContext ctxt) throws IOException {
        return Lang.getLanguage(p.getValueAsString()).orElse(null);
    }
}
