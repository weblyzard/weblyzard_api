package com.weblyzard.api.datatype;

import static org.junit.Assert.*;

import java.util.Arrays;
import java.util.Comparator;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import org.junit.Test;

public class MD5DigestTest {

    @Test
    public void testCompare() {
        final MD5Digest mid = MD5Digest.fromHexDigest("38338baad6b2c8864e969803250d2391");
        final MD5Digest larger1 = MD5Digest.fromHexDigest("38338baad6b2c8864e969803250d2392");
        final MD5Digest larger2 = MD5Digest.fromHexDigest("38338baad6b2c8874e969803250d2391");

        // direct compare
        assertTrue(mid.compare(mid, mid) == 0);
        assertTrue(mid.compare(mid, larger1) == -1);
        assertTrue(mid.compare(mid, larger2) == -1);
        assertTrue(mid.compare(larger1, mid) == 1);
        assertTrue(mid.compare(larger2, mid) == 1);

        assertTrue(mid.compare(larger1, larger1) == 0);
        assertTrue(mid.compare(larger2, larger2) == 0);

        // sorting using Comparator
        List<MD5Digest> lst = Arrays.asList(larger2, mid, larger1);
        lst.sort(new MD5Digest());
        assertNotEquals(Arrays.asList(larger2, mid, larger1), lst);
        assertEquals(Arrays.asList(mid, larger1, larger2), lst);

        // sorting using Comparable
        lst =
                Stream.of(larger2, mid, larger1)
                        .sorted(Comparator.naturalOrder())
                        .collect(Collectors.toList());
        assertNotEquals(Arrays.asList(larger2, mid, larger1), lst);
        assertEquals(Arrays.asList(mid, larger1, larger2), lst);
    }

    @Test
    @SuppressWarnings("unlikely-arg-type")
    public void testEquals() {
        final MD5Digest mid = MD5Digest.fromHexDigest("38338baad6b2c8864e969803250d2391");
        final MD5Digest larger1 = MD5Digest.fromHexDigest("38338baad6b2c8864e969803250d2392");

        // tests
        assertTrue(mid.equals(mid));
        assertTrue(larger1.equals(larger1));
        assertFalse(mid.equals(larger1));

        assertFalse(mid.equals(null));
        assertFalse(mid.equals("test"));
    }
}
