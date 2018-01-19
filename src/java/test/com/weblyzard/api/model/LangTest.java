package com.weblyzard.api.model;

import static org.junit.Assert.assertEquals;
import java.util.Optional;
import org.junit.Test;

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
