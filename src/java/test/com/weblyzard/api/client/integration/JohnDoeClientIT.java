package com.weblyzard.api.client.integration;

import static org.junit.Assert.assertTrue;

import java.util.Arrays;
import java.util.List;

import org.junit.Before;
import org.junit.Test;

import com.weblyzard.api.client.JohnDoeClient;
import com.weblyzard.api.client.WebserviceClientConfig;
import com.weblyzard.api.model.johndoe.JohnDoeDocument;

public class JohnDoeClientIT {
	
	private JohnDoeClient client;
	private static final String TEST_PROFILE = "JOBCOCKPIT";
	private static final String TEST_BASEURL = "http://www.tbd.com";
	private JohnDoeDocument document; 
	
	@Before
	public void setUp() {
		List<String> names = Arrays.asList(new String[] {"Michael Novizki", "Anna Skruptsch","Michael Peter Landon"});
		document = new JohnDoeDocument(TEST_PROFILE, TEST_BASEURL,names);
		client = new JohnDoeClient(
		        new WebserviceClientConfig().setUrl("http://localhost").setServicePrefix(":63014"));
	}
	
	@Test
	public void johnDoeClientTestIT() {
		JohnDoeDocument resultDocument = client.annonymizeContent(document);
		assertTrue(resultDocument != null);
		assertTrue(resultDocument.getNameAnnonIdMap().size() == 3);
	}
}
