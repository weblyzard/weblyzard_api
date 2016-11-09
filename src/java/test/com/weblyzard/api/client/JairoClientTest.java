package com.weblyzard.api.client;

import static org.junit.Assert.*;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import org.junit.Test;

import com.weblyzard.api.document.annotation.Annotation;

public class JairoClientTest {

	private static final String profileName = "test";



	@Test
	public void testExtendAnnotation1() {
		JairoClient client = new JairoClient();

		List<Annotation> annotations = new ArrayList<>(
				Arrays.asList(new Annotation().setKey("<" + "http://dbpedia.org/resource/Aurora_(singer)" + ">")));

		List<Annotation> result = client.extendAnnotations(profileName, annotations);
		assertTrue(result.size() > 0);
	}



	@Test
	public void testExtendAnnotation2() {
		JairoClient client = new JairoClient();

		List<Annotation> annotations = new ArrayList<>(
				Arrays.asList(new Annotation().setKey("<" + "http://dbpedia.org/resource/Feusisberg" + ">"),
						new Annotation().setKey("<" + "http://dbpedia.org/resource/Shani_Tarashaj" + ">"),
						new Annotation().setKey(
								"<" + "http://dbpedia.org/resource/Grasshopper_Club_Zürich__Shani_Tarashaj__1" + ">"),
						new Annotation().setKey("<" + "http://dbpedia.org/resource/Bruno_Schweizer" + ">")));

		List<Annotation> result = client.extendAnnotations(profileName, annotations);
		assertTrue(result != null);
	}

}