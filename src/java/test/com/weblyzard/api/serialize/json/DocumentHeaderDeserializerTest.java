package com.weblyzard.api.serialize.json;

import static org.junit.jupiter.api.Assertions.assertTrue;
import java.io.IOException;
import java.util.InvalidPropertiesFormatException;
import javax.xml.namespace.QName;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.KeyDeserializer;

public class DocumentHeaderDeserializerTest {

    KeyDeserializer deserializer = new DocumentHeaderDeserializer();

    @Test
    public void testSupportedPrefix() throws JsonProcessingException, IOException {
        Assertions.assertThrows(InvalidPropertiesFormatException.class,
                () -> deserializer.deserializeKey("wl:jonas_type", null));
    }

    @Test
    public void testSupportedNamespace() throws JsonProcessingException, IOException {
        Assertions.assertThrows(InvalidPropertiesFormatException.class, () -> deserializer
                .deserializeKey("http://www.weblyzard.com/wl/2013#jonas_type", null));
    }

    @Test
    public void testSupportedNamespaceInBrackets() throws JsonProcessingException, IOException {
        QName result = (QName) deserializer
                .deserializeKey("{http://www.weblyzard.com/wl/2013#}jonas_type", null);
        assertTrue(result.getLocalPart().equals("jonas_type"));
        assertTrue(result.getNamespaceURI().equals("http://www.weblyzard.com/wl/2013#"));
        assertTrue(result.getPrefix().equals(""));
    }

    @Test
    public void testUnknownNamespaceInBrackets() throws JsonProcessingException, IOException {
        QName result = (QName) deserializer.deserializeKey("{http://foo.bar/test#}test", null);
        assertTrue(result.getLocalPart().equals("test"));
        assertTrue(result.getNamespaceURI().equals("http://foo.bar/test#"));
        assertTrue(result.getPrefix().equals(""));
    }
}
