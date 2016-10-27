package com.weblyzard.api.joel;

import java.util.List;

import javax.ws.rs.client.Client;
import javax.ws.rs.client.ClientBuilder;
import javax.ws.rs.client.Entity;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;

import com.weblyzard.api.document.Document;

public class JoelClient {
	
	private String baseURL; 
	
	private Client client; 
	
	public JoelClient(String baseURL) {
		this.baseURL = baseURL;
		client = ClientBuilder.newClient(); 
	}
	
	public String getBaseURL() {
		return baseURL;
	}

	public Response status() {
		return client
			.target(baseURL)
			.path("status")
			.request(MediaType.APPLICATION_JSON_TYPE)
			.get();
	}	
	
	public Response addDocuments(List<Document> documents) {
		return client
			.target(baseURL)
			.path("addDocuments")
			.request(MediaType.APPLICATION_JSON_TYPE)
			.post(Entity.json(documents)); 		
	}
}
