package com.weblyzard.api.model.document.partition;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertTrue;
import java.io.IOException;
import java.net.URL;
import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.Test;
import com.fasterxml.jackson.core.JsonParseException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.JsonMappingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.google.common.io.Resources;

/**
 * Ensures compatibility between different sentence annotation specifications.
 * 
 * @author Albert Weichselbraun
 *
 */
class SentenceCharSpanTest {

    private static final String JSON_EXAMPLE_DIR = "json/";
    private static final ObjectMapper MAPPER = new ObjectMapper();

    @Test
    void testSentencesWithoutAnnotations() throws JsonParseException, JsonMappingException, IOException {
        List<SentenceCharSpan> sentenceCharSpanList = getSentenceCharSpan("sentence-without-annotations.json");
        assertEquals(4, sentenceCharSpanList.size());
        int lastStartIndex = -1;
        int lastEndIndex = -1;
        for (SentenceCharSpan s : sentenceCharSpanList) {
            assertTrue(lastStartIndex < s.getStart());
            assertTrue(lastEndIndex < s.getEnd());
            lastStartIndex = s.getStart();
            lastEndIndex = s.getEnd();
            assertNull(s.getNumericSentenceProperties());
        }
    }

    @Test
    void testSentencesWithStandardAnnotations() throws JsonParseException, JsonMappingException, IOException {
        List<SentenceCharSpan> sentenceCharSpanList = getSentenceCharSpan("sentence-with-standard-annotations.json");
        assertEquals(4, sentenceCharSpanList.size());
        int lastStartIndex = -1;
        int lastEndIndex = -1;
        for (SentenceCharSpan s : sentenceCharSpanList) {
            assertTrue(lastStartIndex < s.getStart());
            assertTrue(lastEndIndex < s.getEnd());
            lastStartIndex = s.getStart();
            lastEndIndex = s.getEnd();
            Map<String, Double> numericSentenceProperties = s.getNumericSentenceProperties();
            assertEquals(0.1, numericSentenceProperties.get("semOrient"));
            assertEquals(0.2, numericSentenceProperties.get("significance"));
        }
    }

    @Test
    void testSentencesWithExtendedAnnotations() throws JsonParseException, JsonMappingException, IOException {
        List<SentenceCharSpan> sentenceCharSpanList = getSentenceCharSpan("sentence-with-extended-annotations.json");
        assertEquals(3, sentenceCharSpanList.size());
        int lastStartIndex = -1;
        int lastEndIndex = -1;
        for (SentenceCharSpan s : sentenceCharSpanList) {
            assertTrue(lastStartIndex < s.getStart());
            assertTrue(lastEndIndex < s.getEnd());
            lastStartIndex = s.getStart();
            lastEndIndex = s.getEnd();
            Map<String, Double> numericSentenceProperties = s.getNumericSentenceProperties();
            assertEquals(0.1, numericSentenceProperties.get("semOrient"));
            assertEquals(0.9, numericSentenceProperties.get("significance"));
        }
        assertEquals(0.8, sentenceCharSpanList.get(0).getNumericSentenceProperties().get("mediaCriticismScore"));
        assertEquals(0.6, sentenceCharSpanList.get(1).getNumericSentenceProperties().get("veracityScore"));
        assertEquals(0.8, sentenceCharSpanList.get(2).getNumericSentenceProperties().get("mediaCriticismScore"));
    }

    private static List<SentenceCharSpan> getSentenceCharSpan(String fname)
                    throws JsonParseException, JsonMappingException, IOException {
        URL r = Resources.getResource(JSON_EXAMPLE_DIR + fname);
        return MAPPER.readValue(r, new TypeReference<List<SentenceCharSpan>>() {});
    }

}
