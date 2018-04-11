package com.weblyzard.api.serialize.json;

import static org.junit.Assert.assertEquals;
import java.io.IOException;
import java.util.Arrays;
import org.junit.Test;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.weblyzard.api.model.Lang;
import com.weblyzard.api.model.document.Document;
import com.weblyzard.api.model.document.StringRange;

public class DocumentSerializationTest {

    private static final ObjectMapper mapper = new ObjectMapper();

    @Test
    public void test() throws IOException {
        final Document document = new Document().setId("007").setFormat("text/html")
                .setLang(Lang.EN)
                .setContent(
                        "Love is patient, love is kind. It does not envy, it does not boast, it is not proud.")
                .setLineIndices(Arrays.asList(new StringRange(0, 74), new StringRange(74, 84)))
                .setSentenceIndices(Arrays.asList(new StringRange(0, 30), new StringRange(31, 84)))
                .setTokenIndices(Arrays.asList(new StringRange(0, 4), new StringRange(5, 7),
                        new StringRange(8, 15), new StringRange(15, 16), new StringRange(17, 21),
                        new StringRange(22, 24), new StringRange(25, 29), new StringRange(29, 30),
                        new StringRange(31, 33), new StringRange(31, 33)));

        // test sentence id/md5sum (MD5Digest)
        testSerialization(document);

    }

    private static void testSerialization(Document document) throws IOException {
        String json = mapper.writeValueAsString(document);
        Document deserializedSentence = mapper.readValue(json, Document.class);
        assertEquals(document, deserializedSentence);
    }
}
