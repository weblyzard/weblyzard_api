package com.weblyzard.api.model;

import static org.junit.Assert.*;

import org.junit.Test;

public class LangTest {

    @Test
    public void test() {
        Lang l = Lang.getLanguage("de");
        assertEquals(Lang.DE, l);
        assertEquals("de", l.toString());
    }
}
