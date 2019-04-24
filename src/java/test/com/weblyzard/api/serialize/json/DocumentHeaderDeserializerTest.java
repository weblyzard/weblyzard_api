package com.weblyzard.api.serialize.json;

import static org.junit.jupiter.api.Assertions.assertTrue;
import java.io.IOException;
import javax.xml.namespace.QName;
import org.junit.jupiter.api.Test;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.KeyDeserializer;

public class DocumentHeaderDeserializerTest {

    KeyDeserializer deserializer = new DocumentHeaderDeserializer();

    @Test
    public void testSupportedPrefix() throws JsonProcessingException, IOException {
        QName result = (QName) deserializer.deserializeKey("wl:jonas_type", null);
        assertTrue(result.getLocalPart().equals("jonas_type"));
        assertTrue(result.getNamespaceURI().equals("http://www.weblyzard.com/wl/2013#"));
        assertTrue(result.getPrefix().equals("wl"));
    }

    @Test
    public void testSupportedNamespace() throws JsonProcessingException, IOException {
        QName result = (QName) deserializer
                .deserializeKey("http://www.weblyzard.com/wl/2013#jonas_type", null);
        assertTrue(result.getLocalPart().equals("jonas_type"));
        assertTrue(result.getNamespaceURI().equals("http://www.weblyzard.com/wl/2013#"));
        assertTrue(result.getPrefix().equals("wl"));
    }

    @Test
    public void testUnknownPrefix() throws JsonProcessingException, IOException {
        QName result = (QName) deserializer.deserializeKey("foo:bar", null);
        assertTrue(result.getLocalPart().equals("foo:bar"));
        assertTrue(result.getNamespaceURI().equals(""));
        assertTrue(result.getPrefix().equals(""));
    }

    @Test
    public void testUnknownNamespace() throws JsonProcessingException, IOException {
        QName result = (QName) deserializer.deserializeKey("http://foo.bar/test#test", null);
        assertTrue(result.getLocalPart().equals("http://foo.bar/test#test"));
        assertTrue(result.getNamespaceURI().equals(""));
        assertTrue(result.getPrefix().equals(""));
    }

}
