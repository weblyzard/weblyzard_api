package com.weblyzard.api.model.annotation;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.google.common.collect.ImmutableList;
import com.google.common.collect.ImmutableMap;
import com.weblyzard.api.datatype.MD5Digest;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.io.IOException;
import org.junit.jupiter.api.Test;

public class AnnotationSerializationTest {

  private static final ObjectMapper MAPPER = new ObjectMapper();

  static {
    MAPPER.enable(SerializationFeature.INDENT_OUTPUT);
  }

  @Test
  public void testJsonSerialization() throws JsonProcessingException, IOException {
    Annotation testAnnotation =
        Annotation.build("http://dbpedia.org/resource/Augustine_of_Hippo")
            .setPreferredName("Augustine of Hippo")
            .setEntityType("PersonEntity")
            .annotation()
            .setSurfaceForm("Saint Augustine")
            .setStart(0)
            .setEnd(0)
            .setSentence(1)
            .setMd5sum(MD5Digest.fromText("Augustine of Hippo was an early Christian theologian."));

    serializeAndCompare(testAnnotation);

    testAnnotation.setEntityMetadata(
        ImmutableMap.of(
            "rdf:type", ImmutableList.of("foaf:Person", "dbo:Person"),
            "foaf:name", ImmutableList.of("Augustine", "St. Augustine")));
    serializeAndCompare(testAnnotation);
  }

  private static void serializeAndCompare(Annotation o) throws IOException {
    String json = MAPPER.writeValueAsString(o);
    System.out.println(json);
    assertEquals(o, MAPPER.readValue(json, Annotation.class));
  }
}
