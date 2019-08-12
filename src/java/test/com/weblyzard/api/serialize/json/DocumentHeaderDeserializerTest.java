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
    public void testUppercasePrefix() throws JsonProcessingException, IOException {
        QName result = (QName) deserializer.deserializeKey("WL:jonas_type", null);
        assertTrue(result.getLocalPart().equals("WL:jonas_type"));
        assertTrue(result.getNamespaceURI().equals(""));
        assertTrue(result.getPrefix().equals(""));
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
    public void testSupportedNamespaceInBrackets() throws JsonProcessingException, IOException {
        QName result = (QName) deserializer
                .deserializeKey("{http://www.weblyzard.com/wl/2013#}jonas_type", null);
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

    @Test
    public void testUnknownNamespaceExt() throws JsonProcessingException, IOException {
        QName result =
                (QName) deserializer.deserializeKey("http://schema.org/people/jonas_type", null);
        assertTrue(result.getLocalPart().equals("http://schema.org/people/jonas_type"),
                String.format("Expected input, but was '%s'", result.getLocalPart()));
        assertTrue(result.getNamespaceURI().equals(""),
                String.format("Expected empty string but was '%s'", result.getNamespaceURI()));
        assertTrue(result.getPrefix().equals(""),
                String.format("Expected empty string but was '%s'", result.getPrefix()));
    }

    @Test
    public void testUnknownNamespaceInBrackets() throws JsonProcessingException, IOException {
        QName result = (QName) deserializer.deserializeKey("{http://foo.bar/test#}test", null);
        assertTrue(result.getLocalPart().equals("test"));
        assertTrue(result.getNamespaceURI().equals("http://foo.bar/test#"));
        assertTrue(result.getPrefix().equals(""));
    }

    @Test
    public void testUnknownNamespaceInBracketsExt() throws JsonProcessingException, IOException {
        QName result =
                (QName) deserializer.deserializeKey("{http://schema.org/people/}jonas_type", null);
        assertTrue(result.getLocalPart().equals("jonas_type"),
                String.format("Expected 'jonas_type' but was '%s'", result.getLocalPart()));
        assertTrue(result.getNamespaceURI().equals("http://schema.org/people/"), String.format(
                "Expected 'http://schema.org/people/' but was '%s'", result.getNamespaceURI()));
        assertTrue(result.getPrefix().equals(""),
                String.format("Expected empty string but was '%s'", result.getPrefix()));
    }

}
