package com.weblyzard.api.serialize.json;

import com.fasterxml.jackson.core.JsonGenerationException;
import com.fasterxml.jackson.core.JsonGenerator;
import com.fasterxml.jackson.databind.SerializerProvider;
import com.fasterxml.jackson.databind.ser.std.StdSerializer;
import com.weblyzard.api.model.annotation.Annotation;
import java.io.IOException;
import java.lang.reflect.Field;
import lombok.extern.slf4j.Slf4j;

/**
 * @author Norman Suesstrunk
 *     <p>Resource:
 *     <p>Solution used:
 *     http://stackoverflow.com/questions/14714328/jackson-how-to-add-custom-property-to-the-json-without-modifying-the-pojo
 *     <p>Possibilities: - https://lewdawson.com/advanced-java-json-deserialization/ -
 *     https://github.com/lewisdawson/java-jackson-serialize-example
 */
@Slf4j
public class AnnotationSerializer extends StdSerializer<Annotation> {

    public static final String ANNOTATION_HEADER_FIELDNAME = "header";

    public AnnotationSerializer() {
        this(null);
    }

    protected AnnotationSerializer(Class<Annotation> t) {
        super(t);
    }

    /** */
    private static final long serialVersionUID = 1L;

    /** {@inheritDoc} */
    @Override
    public void serialize(
            Annotation annotation,
            JsonGenerator jsonGenerator,
            SerializerProvider serializerProvider)
            throws IOException, JsonGenerationException {

        jsonGenerator.writeStartObject();
        Field[] fields = annotation.getClass().getDeclaredFields();

        // use class inspection to write the fields
        for (Field field : fields) {
            // only write the field if it is not the map field ("enriched fields" in Annotation class)

            if (!field.getName().equals(ANNOTATION_HEADER_FIELDNAME)) {
                try {
                    field.setAccessible(true);
                    jsonGenerator.writeObjectField(field.getName(), field.get(annotation));
                } catch (IllegalArgumentException | IllegalAccessException e) {
                    log.warn("Cannot serialize Annotation: {}", e.getLocalizedMessage());
                }
            } else {
                // add the enriched fields
                for (String key : annotation.getHeader().keySet()) {
                    jsonGenerator.writeObjectField(key, annotation.getHeader().get(key));
                }
            }
        }
        jsonGenerator.writeEndObject();
    }
}
