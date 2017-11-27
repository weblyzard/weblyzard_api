package com.weblyzard.api.model;

import static org.junit.Assert.*;

import java.util.Optional;

import org.junit.Test;

public class RegionTest {
    @Test
    public void test() {
        Region l = Region.getRegion("ch").get();
        assertEquals(Region.CH, l);
        assertEquals("CH", l.toString());
    }

    @Test
    public void testIllegalRegions() {
        // null pointer language
        assertEquals(Optional.empty(), Region.getRegion(null));

        // non existent language
        assertEquals(Optional.empty(), Region.getRegion("invalid"));
    }

}
