package com.weblyzard.lib;

import java.io.IOException;

import com.fasterxml.jackson.core.JsonParser;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.DeserializationContext;
import com.fasterxml.jackson.databind.deser.std.StdDeserializer;

public class MD5DigestJsonDS extends StdDeserializer<MD5Digest> {

	private static final long serialVersionUID = 1L;

	public MD5DigestJsonDS() {
		this(null); 
	}
	
	protected MD5DigestJsonDS(Class<?> vc) {
		super(vc);
	}

	@Override
	public MD5Digest deserialize(JsonParser p, DeserializationContext ctxt)
			throws IOException, JsonProcessingException {
		return MD5Digest.fromText(p.getValueAsString());
	}
}
