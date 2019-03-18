package com.weblyzard.api.serialize.json;

import static org.junit.jupiter.api.Assertions.assertEquals;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.weblyzard.api.model.document.Sentence;
import java.io.IOException;
import org.junit.jupiter.api.Test;

public class SerializationTest {

  private static final ObjectMapper mapper = new ObjectMapper();

  @Test
  public void test() throws IOException {
    final Sentence sentence =
        new Sentence(
            "McChain (former US presidente candidate) stated that he would strongly support such actions.",
            "0,7 8,9 9,15 16,18 19,29 30,39 39,40 41,47 48,52 53,55 56,61 62,70 71,78 79,83 84,91 91,92",
            "NNP ( JJ NNP NN NN ) VBD IN PRP MD RB VB JJ NNS .");

    // test sentence id/md5sum (MD5Digest)
    testSerialization(sentence);

    // test isTitle attribute (BooleanAdapter)
    sentence.setTitle(false);
    testSerialization(sentence);

    sentence.setTitle(true);
    testSerialization(sentence);
  }

  private static void testSerialization(Sentence sentence) throws IOException {
    String json = mapper.writeValueAsString(sentence);
    Sentence deserializedSentence = mapper.readValue(json, Sentence.class);
    assertEquals(sentence, deserializedSentence);
  }
}
