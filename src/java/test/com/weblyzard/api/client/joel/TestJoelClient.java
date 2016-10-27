package com.weblyzard.api.client.joel;

import static org.junit.Assert.assertNotNull;

import java.util.ArrayList;
import java.util.List;
import java.util.logging.Logger;

import javax.ws.rs.core.Response;

import org.junit.Before;
import org.junit.Test;

import com.weblyzard.api.document.Document;

public class TestJoelClient extends JoelTestBase {
	
	Logger logger = Logger.getLogger(getClass().getName());
	
	private JoelClient joelClient; 

	@Before
	public void before() {
		joelClient = new JoelClient("http://localhost:8080");
	}
	
	@Test
	public void testJoelClientClustering() {
		Response statusResponse = joelClient.addDocuments(psalmDocs);
		assertNotNull(statusResponse);
		logger.info(statusResponse.toString());
	}
	
	@Test
	public void testJoelClient() {
		Response statusResponse = joelClient.status(); 
		assertNotNull(statusResponse);
		logger.info(statusResponse.toString());
	}
	
	@Test
	public void testJoelClientWithDocuments(){
		List<Document> documents = new ArrayList<>();
		documents.add(new Document("nuclear power plant"));
		Response statusResponse = joelClient.addDocuments(documents);
		assertNotNull(statusResponse);
		logger.info(statusResponse.toString());
	}
}
