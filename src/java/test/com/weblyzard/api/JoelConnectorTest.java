package com.weblyzard.api;

import static org.junit.Assert.*;

import java.io.IOException;
import java.util.HashSet;
import java.util.Set;

import javax.ws.rs.core.Response;
import javax.xml.bind.JAXBException;

import org.apache.http.auth.AuthenticationException;
import org.apache.http.client.ClientProtocolException;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import com.google.gson.JsonObject;
import com.weblyzard.api.domain.weblyzard.Document;

public class JoelConnectorTest {

	JoelConnector connector = new JoelConnector();



	@Test
	@Before
	public void testAddDocuments() throws AuthenticationException, ClientProtocolException, IOException, JAXBException {
		Set<Document> documents = new HashSet<>();
		documents.add(new Document(""));
		documents.add(new Document(""));

		Response response = connector.callAddDocuments(documents);
		assertTrue(response.getStatus() == 200);
	}



	@Test
	public void testCluster() throws AuthenticationException, ClientProtocolException, IOException, JAXBException {
		JsonObject response = connector.callCluster();
		assertTrue(response != null);
	}



	@Test
	@After
	public void testFlush() throws AuthenticationException, ClientProtocolException, IOException, JAXBException {
		Response response = connector.callFlush();
		assertTrue(response.getStatus() == 200);
	}

}
