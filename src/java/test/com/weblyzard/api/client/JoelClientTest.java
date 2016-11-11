package com.weblyzard.api.client;

import static org.junit.Assert.assertTrue;

import java.io.IOException;
import java.util.List;
import java.util.logging.Logger;

import javax.ws.rs.ClientErrorException;
import javax.xml.bind.JAXBException;

import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.*;

import com.fasterxml.jackson.core.JsonParseException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.JsonMappingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.weblyzard.api.document.Document;
import com.weblyzard.api.joel.ClusterResult;

/**
 * 
 * @author norman.suesstrunk@htwchur.ch
 *
 */
public class JoelClientTest {
	
	private static final String PSALMS_DOCS_WEBLYZARDFORMAT_JSON = "resources/psalms-docs-weblyzardformat.json";

	public List<Document> psalmDocs;
	
	private Logger logger = Logger.getLogger(getClass().getName()); 
	
	private JoelClient joelClient; 
	
	@Before
	public void before() {
		psalmDocs = readWeblyzardDocuments();
		joelClient = new JoelClient(); 
	}
	
	@Test 
	public void testJoelWorkflow() {
		try {
			
			// 1. send the psalmDocs to the joel 
			joelClient.addDocuments(psalmDocs);
			
			// 2. cluster the documents  
			List<ClusterResult> clusterResults = joelClient.cluster(); 
			assertTrue(clusterResults.size()>0);
			
			// flush the queue 
			assertEquals(200, joelClient.flush().getStatus()); 
			
			
		} catch (ClientErrorException | JAXBException e) {
			e.printStackTrace();
		} 
	}
	
	
	
	public List<Document> readWeblyzardDocuments() {
		try {

			logger.info(JoelClientTest.class.getClassLoader().getResource(".").getPath());
			ObjectMapper objectMapper = new ObjectMapper();
			objectMapper.configure(SerializationFeature.FAIL_ON_EMPTY_BEANS, false);
			return objectMapper.readValue(JoelClientTest.class.getClassLoader().getResourceAsStream(
					PSALMS_DOCS_WEBLYZARDFORMAT_JSON), new TypeReference<List<Document>>() {
					});
		}
		catch (JsonParseException e1) {
			e1.printStackTrace();
		} catch (JsonMappingException e1) {
			e1.printStackTrace();
		} catch (IOException e1) {
			e1.printStackTrace();
		}
		return null;
	}
}
