package com.weblyzard.api.datatype;

import java.io.Serializable;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

import javax.xml.bind.DatatypeConverter;
import javax.xml.bind.annotation.adapters.XmlAdapter;

import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import com.fasterxml.jackson.databind.annotation.JsonSerialize;
import com.google.common.primitives.Longs;
import com.weblyzard.api.document.serialize.json.MD5DigestDeserializer;
import com.weblyzard.api.document.serialize.json.MD5DigestSerializer;

/**
 * A performance and memory optimized representation of MD5Digests.
 * @author Albert Weichselbraun <albert.weichselbraun@htwchur.ch>
 *
 */

@JsonSerialize(using = MD5DigestSerializer.class)
@JsonDeserialize (using = MD5DigestDeserializer.class)
public class MD5Digest extends XmlAdapter<String, MD5Digest> implements Serializable{
	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	// the md5sum's values
	private long low, high;
	
	public MD5Digest(byte[] m) {
		high = Longs.fromBytes(m[0], m[1], m[2], m[3], m[4], m[5], m[6], m[7]);
		low= Longs.fromBytes(m[8],m[9], m[10],m[11],m[12],m[13],m[14],m[15]);
	}
	
	// required for JAXB
	public MD5Digest() {
	}
	
	/**
	 * Creates an MD5Digest from a hexString
	 * @param hexString
	 * @return 
	 * 	the corresponding MD5Digest object
	 */
	public static MD5Digest fromHexDigest(String hexString) {
		byte[] messageDigest = DatatypeConverter.parseHexBinary(hexString);
		return new MD5Digest(messageDigest);
	}
	
	/**
	 * Computes the MD5 digest of the given String.
	 * @param text
	 * @return
	 */
	public static MD5Digest fromText(String text) {
		return new MD5Digest(getMessageDigest().digest(text.getBytes()));
	}
	
	@Override
	public int hashCode() {
		return (int)(low^(low>>>32)^high^(high>>>32));
	}
	
	@Override
	public boolean equals(Object o) {
		try {
			MD5Digest m = (MD5Digest) o;
			return low == m.low && high == m.high;
		} catch (ClassCastException | NullPointerException e) {
			return false;
		}
	}
	
	@Override
	public String toString() {
		return String.format("%016X%016X", high, low).toLowerCase();
	}
	
	/* 
	 * @return a message digest instance
	 */
	public static MessageDigest getMessageDigest() {
		try {
			return MessageDigest.getInstance("MD5");
		} catch (NoSuchAlgorithmException e) {
			e.printStackTrace();
			return null;
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
	
}
