package com.weblyzard.api.client;

import java.util.List;

import javax.ws.rs.WebApplicationException;
import javax.ws.rs.client.Entity;
import javax.ws.rs.core.GenericType;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import javax.xml.bind.JAXBException;

import com.weblyzard.api.document.Document;
import com.weblyzard.api.joel.ClusterResult;

/**
 * 
 * @author philipp.kuntschik@htwchur.ch, norman.suesstrunk@htwchur.ch
 *
 */
public class JoelClient extends BasicClient {

	private static final String ADDDOCUMENTS_SERVICE_URL = "/joel/rest/addDocuments";
	private static final String CLUSTER_DOCUMENT_SERVICEURL = "/joel/rest/cluster";
	private static final String FLUSH_DOCUMENT_SERVICE_URL = "/joel/rest/flush";


	/**
	 * @see BasicClient
	 */
	public JoelClient() {
		super();
	}
	public JoelClient(String weblyzard_url) {
		super(weblyzard_url);
	}

	public JoelClient(String weblyzard_url, String username, String password) {
		super(weblyzard_url, username, password);
	}

	public Response addDocuments(List<Document> documents) throws WebApplicationException, JAXBException {
		Response response = super.target.path(ADDDOCUMENTS_SERVICE_URL).request(MediaType.APPLICATION_JSON_TYPE)
				.post(Entity.json(documents));
		super.checkResponseStatus(response);
		response.close(); 
		return response;
	}


	public Response flush() throws WebApplicationException {
		Response response = super.target.path(FLUSH_DOCUMENT_SERVICE_URL).request(MediaType.APPLICATION_JSON_TYPE).get();
		super.checkResponseStatus(response);
		response.close();
		return response;
	}



	public List<ClusterResult> cluster() throws WebApplicationException {
		Response response = super.target.path(CLUSTER_DOCUMENT_SERVICEURL).request(MediaType.APPLICATION_JSON_TYPE).get();
		super.checkResponseStatus(response);
		List<ClusterResult> clusterResults = response.readEntity(new GenericType<List<ClusterResult>>() {});
		response.close();
		return clusterResults;
	}
}
