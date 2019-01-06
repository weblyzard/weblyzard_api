package com.weblyzard.api.client.integration;

import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.Arrays;
import java.util.List;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import com.weblyzard.api.client.JohnDoeClient;
import com.weblyzard.api.client.WebserviceClientConfig;
import com.weblyzard.api.model.johndoe.JohnDoeDocument;

public class JohnDoeClientIT {
	
	private JohnDoeClient client;
	private static final String TEST_PROFILE = "JOBCOCKPIT";
	private static final String TEST_BASEURL = "http://www.tbd.com";
	private JohnDoeDocument document; 
	
	@BeforeEach
	public void setUp() {
		List<String> names = Arrays.asList(new String[] {"Michael Novizki", "Anna Skruptsch","Michael Peter Landon"});
		document = new JohnDoeDocument(TEST_PROFILE, TEST_BASEURL,names);
		client = new JohnDoeClient(
		        new WebserviceClientConfig().setUrl("http://localhost").setServicePrefix(":63014"));
	}
	
	@Test
	public void johnDoeClientTestIT() {
		JohnDoeDocument resultDocument = client.annonymizeContent(document);
		assertNotNull(resultDocument);
		assertTrue(resultDocument.getNameAnnonIdMap().size() == 3);
	}
}
