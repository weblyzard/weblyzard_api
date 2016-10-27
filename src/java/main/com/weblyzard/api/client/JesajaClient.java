package com.weblyzard.api.client;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import javax.ws.rs.ClientErrorException;
import javax.ws.rs.client.Entity;
import javax.ws.rs.core.GenericType;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;

import com.google.gson.JsonObject;
import com.weblyzard.api.document.Document;

public class JesajaClient extends BasicClient {

	private static final String GETKEYWORDS_SERVICEURL = "/jesaja/rest/get_keywords/";
	private static final String SETREFERENCECORPUS_SERVICEURL = "/jesaja/rest/add_csv/";
	private static final String ADDDOCUMENTS_SERVICEURL = "/jesaja/rest/add_documents/";
	private static final String GETNEKANNOTATIONS_SERVICEURL = "/jesaja/rest/get_nek_annotations/";



	/**
	 * @see BasicClient
	 */
	public JesajaClient() {
		super();
	}



	/**
	 * @see BasicClient
	 */
	public JesajaClient(String weblyzard_url) {
		super(weblyzard_url);
	}



	/**
	 * @see BasicClient
	 */
	public JesajaClient(String weblyzard_url, String username, String password) {
		super(weblyzard_url, username, password);
	}



	public Response setReferenceCorpus(String matviewId, Map<String, Integer> corpusMapping)
			throws ClientErrorException {

		Response response = super.target.path(SETREFERENCECORPUS_SERVICEURL + matviewId)
				.request(MediaType.APPLICATION_JSON_TYPE).post(Entity.json(corpusMapping));

		super.checkResponseStatus(response);
		response.close();

		return response;
	}



	public Response addDocuments(String matviewId, List<Document> documents) throws ClientErrorException {

		Response response = super.target.path(ADDDOCUMENTS_SERVICEURL + matviewId)
				.request(MediaType.APPLICATION_JSON_TYPE).post(Entity.json(documents));

		super.checkResponseStatus(response);
		response.close();

		return response;
	}



	public Map<String, Map<String, Double>> getKeywords(String matviewId, List<Document> documents)
			throws ClientErrorException {

		List<String> xml = new ArrayList<>();
		for (Document document : documents)
			xml.add(Document.getXmlRepresentation(document));

		Response response = super.target.path(GETKEYWORDS_SERVICEURL + matviewId)
				.request(MediaType.APPLICATION_JSON_TYPE).post(Entity.json(xml));

		super.checkResponseStatus(response);
		Map<String, Map<String, Double>> result = response
				.readEntity(new GenericType<Map<String, Map<String, Double>>>() {
				});
		response.close();

		return result;
	}



	public JsonObject call_getNonEntityKeywordAnnotations(String matviewId, List<Document> documents)
			throws ClientErrorException {

		List<String> xml = new ArrayList<>();
		for (Document document : documents)
			xml.add(Document.getXmlRepresentation(document));

		Response response = super.target.path(GETNEKANNOTATIONS_SERVICEURL + matviewId)
				.request(MediaType.APPLICATION_JSON_TYPE).post(Entity.json(xml));

		super.checkResponseStatus(response);
		JsonObject result = response.readEntity(JsonObject.class);
		response.close();
		return result;
	}

}
