package com.weblyzard.api.client;

import java.util.ArrayList;
import java.util.List;

import javax.ws.rs.ClientErrorException;
import javax.ws.rs.client.Entity;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;

import com.google.gson.JsonArray;
import com.weblyzard.lib.document.Document;

/**
 * 
 * @author philipp.kuntschik@htwchur.ch
 *
 */
public class JoelClient extends BasicClient {

	private static final String ADDDOCUMENTSSERVICEURL = "/joel/rest/addDocuments";
	private static final String CLUSTERDOCUMENTSERVICEURL = "/joel/rest/cluster";
	private static final String FLUSHDOCUMENTSERVICEURL = "/joel/rest/flush";



	/**
	 * @see BasicClient
	 */
	public JoelClient() {
		super();
	}



	/**
	 * @see BasicClient
	 */
	public JoelClient(String weblyzard_url) {
		super(weblyzard_url);
	}



	/**
	 * @see BasicClient
	 */
	public JoelClient(String weblyzard_url, String username, String password) {
		super(weblyzard_url, username, password);
	}



	public Response addDocuments(List<Document> documents) throws ClientErrorException {

		List<String> xml = new ArrayList<>();
		for (Document document : documents)
			xml.add(Document.getXmlRepresentation(document));

		// TODO: compare xml with documents (size, .. )

		Response response = super.target.path(ADDDOCUMENTSSERVICEURL).request(MediaType.APPLICATION_JSON_TYPE)
				.post(Entity.json(xml));

		super.checkResponseStatus(response);
		response.close();

		return response;
	}



	public Response flush() throws ClientErrorException {

		Response response = super.target.path(FLUSHDOCUMENTSERVICEURL).request(MediaType.APPLICATION_JSON_TYPE).get();

		super.checkResponseStatus(response);
		response.close();

		return response;
	}



	public JsonArray cluster() throws ClientErrorException {

		Response response = super.target.path(CLUSTERDOCUMENTSERVICEURL).request(MediaType.APPLICATION_JSON_TYPE).get();

		super.checkResponseStatus(response);
		JsonArray result = response.readEntity(JsonArray.class);
		response.close();

		return result;
	}
}
