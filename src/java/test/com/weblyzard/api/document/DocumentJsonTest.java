package com.weblyzard.api.document;


import com.fasterxml.jackson.databind.ObjectMapper;
import com.google.common.base.Charsets;
import com.google.common.io.Resources;
import com.weblyzard.api.model.document.LegacyDocument;
import com.weblyzard.api.model.document.Sentence;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.io.IOException;
import java.net.URL;
import javax.xml.bind.JAXBException;
import javax.xml.namespace.QName;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

/**
 * Tests the serialization to json and the deserialization from json. Tests specifically for the
 * Document.header field as this field uses custom serializers/deserializers
 *
 * @author Norman Süsstrunk
 */
public class DocumentJsonTest {

    public static final URL WEBLYZARD_EXAMPLE_XML =
            DocumentJsonTest.class.getClassLoader().getResource("reference/weblyzard-example.xml");

    private LegacyDocument referenceDocument;
    private QName referenceKeywordQName;
    private final ObjectMapper mapper = new ObjectMapper();

    @BeforeEach
    public void before() throws IOException, JAXBException {

        // init mock objects
        referenceDocument =
                LegacyDocument.fromXml(
                        Resources.toString(WEBLYZARD_EXAMPLE_XML, Charsets.UTF_8));

        referenceKeywordQName =
                new QName(
                        LegacyDocument.WL_KEYWORD_ATTR.getNamespaceURI(),
                        LegacyDocument.WL_KEYWORD_ATTR.getLocalPart());

        // set the header
        referenceDocument.getHeader().put(referenceKeywordQName, "keyword1, keyword2");
    }

    @Test
    public void testSentenceSerialization() throws IOException {
        Sentence sentence = referenceDocument.getSentences().get(0);
        String sentenceJsonSerialized = mapper.writeValueAsString(sentence);
        Sentence deserializedSentence = mapper.readValue(sentenceJsonSerialized, Sentence.class);
        assertEquals(sentence, deserializedSentence);
    }

    @Test
    public void testDocumentSerialization() throws IOException {
        // serialize reference document to String
        String documentJsonSerialized = mapper.writeValueAsString(referenceDocument);

        System.out.println(documentJsonSerialized);

        // deserialize document
        LegacyDocument deserializedDocument = mapper.readValue(documentJsonSerialized, LegacyDocument.class);
        QName deserializedQname = deserializedDocument.getHeader().keySet().iterator().next();

        // must be the same qname
        assertEquals(referenceKeywordQName, deserializedQname);
    }
}
