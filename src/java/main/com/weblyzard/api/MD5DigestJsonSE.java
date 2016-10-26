package com.weblyzard.api;

import java.io.IOException;

import com.fasterxml.jackson.core.JsonGenerationException;
import com.fasterxml.jackson.core.JsonGenerator;
import com.fasterxml.jackson.databind.SerializerProvider;
import com.fasterxml.jackson.databind.ser.std.StdSerializer;

public class MD5DigestJsonSE extends StdSerializer<MD5Digest>{

	private static final long serialVersionUID = 1L;

	public MD5DigestJsonSE() {
		this(null); 
	}
	
	protected MD5DigestJsonSE(Class<MD5Digest> t) {
		super(t);
	}

	@Override
	public void serialize(MD5Digest value, JsonGenerator jgen, SerializerProvider provider)
			throws IOException, JsonGenerationException {
		jgen.writeString(value.toString());
	}
}
