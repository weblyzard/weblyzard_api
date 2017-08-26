package com.weblyzard.api.datatype;

import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import com.fasterxml.jackson.databind.annotation.JsonSerialize;
import com.weblyzard.api.serialize.json.MD5DigestDeserializer;
import com.weblyzard.api.serialize.json.MD5DigestSerializer;
import java.io.Serializable;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.Comparator;
import javax.xml.bind.DatatypeConverter;
import javax.xml.bind.annotation.adapters.XmlAdapter;

/**
 * A performance and memory optimized representation of MD5Digests.
 *
 * @author albert.weichselbraun@htwchur.ch
 */
@JsonSerialize(using = MD5DigestSerializer.class)
@JsonDeserialize(using = MD5DigestDeserializer.class)
public class MD5Digest extends XmlAdapter<String, MD5Digest>
        implements Serializable, Comparator<MD5Digest>, Comparable<MD5Digest> {

    private static final long serialVersionUID = 1L;

    private long low, high;

    public MD5Digest(byte[] m) {
        high = fromBytes(m[0], m[1], m[2], m[3], m[4], m[5], m[6], m[7]);
        low = fromBytes(m[8], m[9], m[10], m[11], m[12], m[13], m[14], m[15]);
    }

    public MD5Digest() {}

    public static MD5Digest fromHexDigest(String hexString) {
        byte[] messageDigest = DatatypeConverter.parseHexBinary(hexString);
        return new MD5Digest(messageDigest);
    }

    public static MD5Digest fromText(String text) {
        return new MD5Digest(getMessageDigest().digest(text.getBytes()));
    }

    @Override
    public int hashCode() {
        return (int) (low ^ (low >>> 32) ^ high ^ (high >>> 32));
    }

    @Override
    public boolean equals(Object o) {
        if (o == null || !(o instanceof MD5Digest)) {
            return false;
        }
        MD5Digest m = (MD5Digest) o;
        return low == m.low && high == m.high;
    }

    @Override
    public String toString() {
        return String.format("%016X%016X", high, low).toLowerCase();
    }

    public static MessageDigest getMessageDigest() {
        try {
            return MessageDigest.getInstance("MD5");
        } catch (NoSuchAlgorithmException e) {
            // MD5 is supported according to the JVM specification
            // this case can never happen...
            throw new RuntimeException("The MD5 message digest is not supported by the JVM.");
        }
    }

    @Override
    public MD5Digest unmarshal(String v) throws Exception {
        return (v == null || v == "") ? null : MD5Digest.fromHexDigest(v);
    }

    @Override
    public String marshal(MD5Digest v) throws Exception {
        return v == null ? "" : v.toString();
    }

    /*
     * 	The {@code long} value of the given big-endian representation of a long.
     *
     * 	This code has been taken from
     *    https://github.com/google/guava/blob/master/guava/src/com/google/common/primitives/Longs.java
     */
    private static long fromBytes(
            byte b1, byte b2, byte b3, byte b4, byte b5, byte b6, byte b7, byte b8) {
        return (b1 & 0xFFL) << 56
                | (b2 & 0xFFL) << 48
                | (b3 & 0xFFL) << 40
                | (b4 & 0xFFL) << 32
                | (b5 & 0xFFL) << 24
                | (b6 & 0xFFL) << 16
                | (b7 & 0xFFL) << 8
                | (b8 & 0xFFL);
    }

    @Override
    public int compare(MD5Digest d1, MD5Digest d2) {
        if (d1.high > d2.high) {
            return 1;
        } else if (d1.high < d2.high) {
            return -1;
        }

        if (d1.low > d2.low) {
            return 1;
        } else if (d1.low < d2.low) {
            return -1;
        }
        return 0;
    }

    @Override
    public int compareTo(MD5Digest o) {
        return compare(this, o);
    }
}
