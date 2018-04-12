package com.weblyzard.api.serialize.json;

import static org.junit.Assert.assertEquals;
import java.io.IOException;
import java.util.Arrays;
import java.util.EnumMap;
import java.util.List;
import java.util.Map;
import org.junit.Test;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.google.common.base.Splitter;
import com.weblyzard.api.model.Lang;
import com.weblyzard.api.model.document.CharSpan;
import com.weblyzard.api.model.document.Dependency;
import com.weblyzard.api.model.document.Document;
import com.weblyzard.api.model.document.DocumentPartition;

public class DocumentSerializationTest {

    private static final ObjectMapper mapper =
            new ObjectMapper().enable(SerializationFeature.INDENT_OUTPUT);
    private static final Splitter SPACE_SPLITTER = Splitter.on(' ');

    @Test
    public void test() throws IOException {
        final Map<DocumentPartition, List<CharSpan>> partitions =
                new EnumMap<>(DocumentPartition.class);
        partitions.put(DocumentPartition.TITLE, Arrays.asList(new CharSpan(0, 20)));
        partitions.put(DocumentPartition.BODY, Arrays.asList(new CharSpan(21, 104)));
        partitions.put(DocumentPartition.LINE,
                Arrays.asList(new CharSpan(0, 20), new CharSpan(21, 94), new CharSpan(95, 106)));
        partitions.put(DocumentPartition.SENTENCE,
                Arrays.asList(new CharSpan(0, 20), new CharSpan(21, 51), new CharSpan(52, 106)));
        partitions.put(DocumentPartition.TOKEN,
                Arrays.asList(new CharSpan(0, 1), new CharSpan(2, 13), new CharSpan(14, 18),
                        new CharSpan(18, 20), new CharSpan(21, 25), new CharSpan(26, 28),
                        new CharSpan(29, 36), new CharSpan(36, 37), new CharSpan(37, 42),
                        new CharSpan(43, 25), new CharSpan(46, 50), new CharSpan(50, 51),
                        new CharSpan(52, 54), new CharSpan(55, 59), new CharSpan(60, 63),
                        new CharSpan(64, 68), new CharSpan(68, 69), new CharSpan(70, 72),
                        new CharSpan(73, 77), new CharSpan(78, 81), new CharSpan(82, 87),
                        new CharSpan(87, 88), new CharSpan(89, 91), new CharSpan(92, 94),
                        new CharSpan(95, 98), new CharSpan(99, 104), new CharSpan(104, 105)));

        final Document document = new Document().setId("007").setFormat("text/html")
                .setLang(Lang.EN)
                .setNilsimsa("1404e487721ca21e08c2141155621022f39a991640a419064123b812a30f2acc")
                .setContent(
                        "1 Corinthians 13:4-7\nLove is patient, love is kind. It does not envy, it does not boast, it is\nnot proud.")
                .setPartitions(partitions)
                .setPos(SPACE_SPLITTER.splitToList(
                        "CD NNP CD CD NN VBZ NN , NN VBZ NN . PRP VBZ RB VB , PRP VBZ RB VB , PRP VBZ RB JJ ."))
                .setDependencies(Arrays.asList(new Dependency(2, "NMOD"), new Dependency(2, "NMOD"),
                        new Dependency(3, "NMOD"), new Dependency(-1, "ROOT"),
                        new Dependency(5, "SBJ"), new Dependency(-1, "ROOT"),
                        new Dependency(5, "PRD"), new Dependency(5, "P"), new Dependency(5, "PRD"),
                        new Dependency(5, "CONJ"), new Dependency(9, "PRD"), new Dependency(5, "P"),
                        new Dependency(12, "SBJ"), new Dependency(-1, "ROOT"),
                        new Dependency(12, "ADV"), new Dependency(12, "VC"),
                        new Dependency(17, "P"), new Dependency(17, "SBJ"),
                        new Dependency(12, "PRD"), new Dependency(17, "ADV"),
                        new Dependency(17, "VC"), new Dependency(22, "P"),
                        new Dependency(22, "SBJ"), new Dependency(12, "PRD"),
                        new Dependency(22, "ADV"), new Dependency(22, "PRD"),
                        new Dependency(12, "P")));


        // test sentence id/md5sum (MD5Digest)
        testSerialization(document);

    }

    private static void testSerialization(Document document) throws IOException {
        String json = mapper.writeValueAsString(document);
        System.out.println(json);
        Document deserializedSentence = mapper.readValue(json, Document.class);
        assertEquals(document, deserializedSentence);
    }
}
