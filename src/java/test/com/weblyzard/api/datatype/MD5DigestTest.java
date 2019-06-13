package com.weblyzard.api.datatype;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.List;
import java.util.Random;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import javax.xml.bind.DatatypeConverter;
import org.junit.jupiter.api.Test;

public class MD5DigestTest {

    private final int SAMPLE_SIZE = 1000;

    @Test
    public void testFromHexDigest() {
        final String text = "Ringstrasse 34, 7000 Chur";
        MD5Digest m = MD5Digest.fromText(text);
        MD5Digest mFromDigest = MD5Digest.fromHexDigest("34acdf2d3df92b5e360159f2f664a9e4");
        assertEquals(m, mFromDigest);
        assertEquals(m.toString(), mFromDigest.toString());
    }

    @Test
    public void testFromText() {
        final String text = "Ringstrasse 34, 7000 Chur";
        MD5Digest m = MD5Digest.fromText(text);
        String md5string = DatatypeConverter.printHexBinary(MD5Digest.getMessageDigest().digest(text.getBytes()));
        assertEquals(md5string.toLowerCase(), m.toString());
    }

    @Test
    public void testEqualsObject() {
        Random rnd = new Random();
        // generate test data
        System.out.println("Generating random testdata.");
        List<String> testData = new ArrayList<>(SAMPLE_SIZE);
        for (int i = 0; i < SAMPLE_SIZE; i++) {
            testData.add("" + rnd.nextLong());
        }
        long time;

        System.out.println("Comparing test data with Strings");
        time = System.nanoTime();
        List<String> digestString = new ArrayList<>(SAMPLE_SIZE);
        for (int i = 0; i < SAMPLE_SIZE; i++) {
            digestString.add(DatatypeConverter
                            .printHexBinary(MD5Digest.getMessageDigest().digest(testData.get(i).getBytes()))
                            .toLowerCase());
        }

        for (int i = 0; i < SAMPLE_SIZE; i++) {
            for (int j = 0; j < SAMPLE_SIZE; j++) {
                if (testData.get(i) != testData.get(j)) {
                    assertNotEquals(digestString.get(i), digestString.get(j));
                } else {
                    assertEquals(digestString.get(i), digestString.get(j));
                }
            }
        }
        System.out.println("Time Required " + (System.nanoTime() - time));

        System.out.println("Comparing test data with MD5Digest");
        time = System.nanoTime();
        List<MD5Digest> digestData = new ArrayList<>(SAMPLE_SIZE);
        for (int i = 0; i < SAMPLE_SIZE; i++) {
            digestData.add(MD5Digest.fromText(testData.get(i)));
        }
        for (int i = 0; i < SAMPLE_SIZE; i++) {
            for (int j = 0; j < SAMPLE_SIZE; j++) {
                if (testData.get(i) != testData.get(j)) {
                    assertNotEquals(digestData.get(i), digestData.get(j));
                } else {
                    assertEquals(digestData.get(i), digestData.get(j));
                }
            }
        }
        System.out.println("Time Required " + (System.nanoTime() - time));

        // ensure that the string representation of the computed
        // md5sums are identical
        for (int i = 0; i < SAMPLE_SIZE; i++) {
            assertEquals(digestData.get(i).toString(), digestString.get(i));
        }
    }

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
        lst = Stream.of(larger2, mid, larger1).sorted(Comparator.naturalOrder()).collect(Collectors.toList());
        assertNotEquals(Arrays.asList(larger2, mid, larger1), lst);
        assertEquals(Arrays.asList(mid, larger1, larger2), lst);
    }

    @Test
    @SuppressWarnings("unlikely-arg-type")
    public void testEquals() {
        final MD5Digest mid = MD5Digest.fromHexDigest("38338baad6b2c8864e969803250d2391");
        final MD5Digest larger1 = MD5Digest.fromHexDigest("38338baad6b2c8864e969803250d2392");

        // test equals
        assertTrue(mid.equals(MD5Digest.fromHexDigest("38338baad6b2c8864e969803250d2391")));
        assertTrue(larger1.equals(MD5Digest.fromHexDigest("38338baad6b2c8864e969803250d2392")));
        assertFalse(mid.equals(larger1));

        assertFalse(mid.equals(null));
        assertFalse(mid.equals("test"));
    }

    @Test
    public void testToString() {
        final MD5Digest digest = MD5Digest.fromHexDigest("0b4591090d210426dbaae959fc5d5df4");
        assertEquals("0b4591090d210426dbaae959fc5d5df4", digest.toString());
    }
}
