package com.weblyzard.api.client.integration;

import static org.junit.Assert.assertTrue;

import org.junit.Before;
import org.junit.Test;

import com.weblyzard.api.client.JohnDoeClient;

public class JohnDoeClientIT {
	
	private JohnDoeClient client;
	private static final String LOCAL_JOHNDOE = "http://localhost:63013";
	private static final String TEST_CONTENT = "Müller Peter Jansen";
	private static final String TEST_PROFILE = "JOBCOCKPIT";
	private static final String TEST_BASEURL = "http://www.tbd.com";
	
	@Before
	public void setUp() {
		client = new JohnDoeClient(LOCAL_JOHNDOE);
	}
	
	@Test
	public void johnDoeClientTestIT() {
		String annonId = client.annonymizeContent(TEST_CONTENT,TEST_PROFILE, TEST_BASEURL);
		assertTrue(annonId != null);
	}
}
