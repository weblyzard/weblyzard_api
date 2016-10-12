package com.weblyzard.api;

import static org.junit.Assert.assertTrue;

import java.io.IOException;
import java.util.Arrays;
import java.util.List;

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
		List<Document> documents = Arrays.asList(new Document(""), new Document(""));

		Response response = connector.call_addDocuments(documents);
		assertTrue(response.getStatus() == 200);
	}



	@Test
	public void testCluster() throws AuthenticationException, ClientProtocolException, IOException, JAXBException {
		JsonObject response = connector.call_cluster();
		assertTrue(response != null);
	}



	@Test
	@After
	public void testFlush() throws AuthenticationException, ClientProtocolException, IOException, JAXBException {
		Response response = connector.call_flush();
		assertTrue(response.getStatus() == 200);
	}

}
