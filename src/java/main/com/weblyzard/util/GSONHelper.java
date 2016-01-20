package com.weblyzard.util;

import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.lang.reflect.Type;

import com.google.gson.Gson;
import com.google.gson.stream.JsonReader;

/**
 * 
 * @author philipp.kuntschik@htwchur.ch
 *
 */
public class GSONHelper {

	private static final String DEFAULTCHARSET = "UTF-8";



	/**
	 * helper to parse an object to its Json-representation
	 * 
	 * @param o
	 *            the object
	 * @param c
	 *            the objecttype
	 * @return the json
	 */
	public static <T> String parseObject(Object o, Class<T> c) {
		final Gson gson = new Gson();
		return gson.toJson(o, c);
	}



	/**
	 * helper to parse an inputstream to its object representation
	 * 
	 * @param inputStream
	 *            inputstream containing the json
	 * @param c
	 *            the objecttype
	 * @return an object of this objecttype
	 * @throws IOException
	 */
	public static <T> Object parseInputStream(InputStream inputStream, Class<T> c) throws IOException {
		return parseInputStream(inputStream, c, DEFAULTCHARSET);
	}



	/**
	 * helper method to parse an inputStream into given class
	 * 
	 * @param inputStream
	 *            The Json-InputStream
	 * @param t
	 *            The targeted class
	 * @return An Object of given class
	 * @throws IOException
	 */
	public static <T> Object parseInputStream(InputStream inputStream, Type t) throws IOException {
		return parseInputStream(inputStream, t, DEFAULTCHARSET);
	}



	/**
	 * helper to parse an inputstream to its object representation
	 * 
	 * @param inputStream
	 *            inputstream containing the json
	 * @param c
	 *            the objecttype
	 * @return an object of this objecttype
	 * @throws IOException
	 */
	public static <T> Object parseInputStream(InputStream inputStream, Class<T> c, String charset) throws IOException {
		final JsonReader reader = new JsonReader(new InputStreamReader(inputStream, charset));
		Object result = new Gson().fromJson(reader, c);
		reader.close();
		inputStream.close();
		return result;
	}



	/**
	 * helper method to parse an inputStream into given class
	 * 
	 * @param inputStream
	 *            The Json-InputStream
	 * @param t
	 *            The targeted class
	 * @return An Object of given class
	 * @throws IOException
	 */
	public static <T> Object parseInputStream(InputStream inputStream, Type t, String charset) throws IOException {
		final JsonReader reader = new JsonReader(new InputStreamReader(inputStream, charset));
		Object result = new Gson().fromJson(reader, t);
		reader.close();
		inputStream.close();
		return result;
	}
}
