package com.weblyzard.api.document;

import java.io.IOException;

import javax.xml.namespace.QName;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.DeserializationContext;
import com.fasterxml.jackson.databind.KeyDeserializer;
import com.fasterxml.jackson.databind.ObjectMapper;

/**
 * 
 * Custom Map Key Deserializer for header field in {@link Document} model class 
 * 
 * The header field in the Document has QName objects as keys 
 * 
 * @author Norman Suesstrunk
 *
 */
public class DocHeaderMapJsonDS extends KeyDeserializer{
	
	private ObjectMapper mapper = new ObjectMapper();

	@Override
	public Object deserializeKey(String key, DeserializationContext ctxt) throws IOException, JsonProcessingException {
		return mapper.readValue(key, QName.class);
	}
}