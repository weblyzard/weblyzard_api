package com.weblyzard.api.document.serialize.json;


import java.io.IOException;
import java.lang.reflect.Field;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import com.fasterxml.jackson.core.JsonGenerationException;
import com.fasterxml.jackson.core.JsonGenerator;
import com.fasterxml.jackson.databind.SerializerProvider;
import com.fasterxml.jackson.databind.ser.std.StdSerializer;
import com.weblyzard.api.document.annotation.CompactAnnotation;

public class CompactAnnotationSerializer extends StdSerializer<CompactAnnotation> {

	public static String ANNOTATION_HEADER_FIELDNAME = "header"; 

	public static List<String> IGNORE_FIELDS = new ArrayList<String>(Arrays.asList("serialVersionUID", 
			"significance", "pos", "start", "end", "surfaceForm", "sentence", "grounded", "scoreName"));
	public CompactAnnotationSerializer() {
		this(null);
	}

	protected CompactAnnotationSerializer(Class<CompactAnnotation> t) {
		super(t);
	}

	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;

	/**
	 * {@inheritDoc}
	 */
	@Override
	public void serialize(CompactAnnotation annotation, JsonGenerator jsonGenerator, SerializerProvider serializerProvider)
			throws IOException, JsonGenerationException {

		jsonGenerator.writeStartObject();
		Iterable<Field> fields = JsonSerializerHelper.getFieldsUpTo(annotation.getClass(), Object.class);


		// use class inspection to write the fields 
		for (Field field : fields) {
			// only write the field if it is not the map field ("enriched fields" in Annotation class)

			if( IGNORE_FIELDS.contains(field.getName()) ) {
				continue;
			}
			if( ! field.getName().equals(ANNOTATION_HEADER_FIELDNAME)) {
				try {
					field.setAccessible(true);
					jsonGenerator.writeObjectField(field.getName(), field.get(annotation));
				} catch (IllegalArgumentException | IllegalAccessException e) {
					e.printStackTrace();
				}
			}
			else {
				// add the enriched fields 
				for(String key: annotation.getHeader().keySet()) {
					// System.out.println("Writing the map field: "+key); 
					jsonGenerator.writeObjectField(key, annotation.getHeader().get(key));
				}
			}
		}
		jsonGenerator.writeEndObject();
	}
}