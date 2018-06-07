package com.weblyzard.api.serialize.xml;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;
import java.io.IOException;
import java.util.Arrays;
import javax.xml.bind.JAXBException;
import org.junit.Test;
import com.weblyzard.api.model.Lang;
import com.weblyzard.api.model.document.LegacyDocument;
import com.weblyzard.api.model.document.LegacySentence;

public class SerializationTest {

    @Test
    public void test() throws IOException, JAXBException {
        final LegacySentence sentence = new LegacySentence(
                "McChain (former US presidente candidate) stated that he would strongly support such actions.",
                "0,7 8,9 9,15 16,18 19,29 30,39 39,40 41,47 48,52 53,55 56,61 62,70 71,78 79,83 84,91 91,92",
                "NNP ( JJ NNP NN NN ) VBD IN PRP MD RB VB JJ NNS .");

        final LegacyDocument document = new LegacyDocument().setId("12").setSentences(Arrays.asList(sentence));

        // test document
        testSerialization(document);

        // language
        document.setLang(Lang.EN);
        testSerialization(document);

        // ensure that the value used for lang is lowercase
        assertTrue(LegacyDocument.toXml(document).contains("lang=\"en\""));
    }

    private static void testSerialization(LegacyDocument document) throws IOException, JAXBException {
        String xmlString = LegacyDocument.toXml(document);
        assertEquals(document, LegacyDocument.fromXml(xmlString));
    }
}
