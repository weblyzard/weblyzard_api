package com.weblyzard.api.model;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.Optional;
import org.junit.jupiter.api.Test;

public class LangTest {

    @Test
    public void test() {
        Lang l = Lang.getLanguage("de").get();
        assertEquals(Lang.DE, l);
        assertEquals("de", l.toString());
    }

    @Test
    public void testIllegalLanguages() {
        // null pointer language
        assertEquals(Optional.empty(), Lang.getLanguage(null));

        // non existent language
        assertEquals(Optional.empty(), Lang.getLanguage("invalid"));
    }
}
