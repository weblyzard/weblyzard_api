package com.weblyzard.api.client.integration;

import org.junit.Before;
import org.junit.Ignore;

import com.weblyzard.api.client.InscriptisClient;

public class InscriptisClientIT extends TestClientBase {
	
	private InscriptisClient inscriptisClient; 
	
	@Before
	public void before() {
		inscriptisClient = new InscriptisClient("http://localhost:5000/");
	}
	
	@Ignore
	public void testInscriptisClient() {
		String parseResult = inscriptisClient.parseHTMl("<html><body><h1>Test Titel</h1></body></html>");
		System.out.println(parseResult);
	}
}
