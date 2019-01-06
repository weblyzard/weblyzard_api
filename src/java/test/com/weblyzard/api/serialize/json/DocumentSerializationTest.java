package com.weblyzard.api.serialize.json;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.io.IOException;
import java.util.EnumMap;
import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.Test;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.weblyzard.api.datatype.MD5Digest;
import com.weblyzard.api.model.Lang;
import com.weblyzard.api.model.Span;
import com.weblyzard.api.model.document.Document;
import com.weblyzard.api.model.document.partition.CharSpan;
import com.weblyzard.api.model.document.partition.Dependency;
import com.weblyzard.api.model.document.partition.DocumentPartition;
import com.weblyzard.api.model.document.partition.SentenceCharSpan;
import com.weblyzard.api.model.document.partition.TokenCharSpan;

public class DocumentSerializationTest {

    private static final ObjectMapper mapper =
            new ObjectMapper().enable(SerializationFeature.INDENT_OUTPUT);

    @Test
    public void test() throws IOException {
        final Map<DocumentPartition, List<Span>> partitions =
                new EnumMap<>(DocumentPartition.class);
        partitions.put(DocumentPartition.TITLE, List.of(new CharSpan(0, 20)));
        partitions.put(DocumentPartition.BODY, List.of(new CharSpan(21, 104)));
        partitions.put(DocumentPartition.LINE,
                List.of(new CharSpan(0, 20), new CharSpan(21, 94), new CharSpan(95, 106)));
        partitions.put(DocumentPartition.SENTENCE,
                List.of(new SentenceCharSpan(0, 20)
                        .setId(MD5Digest.fromHexDigest("75c3e1e742f17035b3577da2305aae32")),
                        new SentenceCharSpan(21, 51)
                                .setId(MD5Digest.fromHexDigest("bce107aa34894c5dbf31c04405a14379")),
                        new SentenceCharSpan(52, 106).setId(
                                MD5Digest.fromHexDigest("822a4044672cf761d98441fb565cc930"))));
        partitions.put(DocumentPartition.TOKEN,
                List.of(new TokenCharSpan(0, 1, "CD", new Dependency(2, "NMOD")),
                        new TokenCharSpan(2, 13, "NNP", new Dependency(2, "NMOD")),
                        new TokenCharSpan(14, 18, "CD", new Dependency(3, "NMOD")),
                        new TokenCharSpan(18, 20, "CD", new Dependency(-1, "ROOT")),
                        new TokenCharSpan(21, 25, "NN", new Dependency(5, "SBJ")),
                        new TokenCharSpan(26, 28, "VBZ", new Dependency(-1, "ROOT")),
                        new TokenCharSpan(29, 36, "NN", new Dependency(5, "PRD")),
                        new TokenCharSpan(36, 37, ",", new Dependency(5, "P")),
                        new TokenCharSpan(37, 42, "NN", new Dependency(5, "PRD")),
                        new TokenCharSpan(43, 25, "VBZ", new Dependency(5, "CONJ")),
                        new TokenCharSpan(46, 50, "NN", new Dependency(9, "PRD")),
                        new TokenCharSpan(50, 51, ".", new Dependency(5, "P")),
                        new TokenCharSpan(52, 54, "PRP", new Dependency(12, "SBJ")),
                        new TokenCharSpan(55, 59, "VBZ", new Dependency(-1, "ROOT")),
                        new TokenCharSpan(60, 63, "RB", new Dependency(12, "ADV")),
                        new TokenCharSpan(64, 68, "VB", new Dependency(12, "VC")),
                        new TokenCharSpan(68, 69, ",", new Dependency(17, "P")),
                        new TokenCharSpan(70, 72, "PRP", new Dependency(17, "SBJ")),
                        new TokenCharSpan(73, 77, "VBZ", new Dependency(12, "PRD")),
                        new TokenCharSpan(78, 81, "RB", new Dependency(17, "ADV")),
                        new TokenCharSpan(82, 87, "VB", new Dependency(17, "VC")),
                        new TokenCharSpan(87, 88, ",", new Dependency(22, "P")),
                        new TokenCharSpan(89, 91, "PRP", new Dependency(22, "SBJ")),
                        new TokenCharSpan(92, 94, "VBZ", new Dependency(12, "PRD")),
                        new TokenCharSpan(95, 98, "RB", new Dependency(22, "ADV")),
                        new TokenCharSpan(99, 104, "JJ", new Dependency(22, "PRD")),
                        new TokenCharSpan(104, 105, ".", new Dependency(12, "P"))));

        final Document document = new Document().setId("007").setFormat("text/html")
                .setLang(Lang.EN)
                .setNilsimsa("1404e487721ca21e08c2141155621022f39a991640a419064123b812a30f2acc")
                .setContent(
                        "1 Corinthians 13:4-7\nLove is patient, love is kind. It does not envy, it does not boast, it is\nnot proud.")
                .setPartitions(partitions);

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
