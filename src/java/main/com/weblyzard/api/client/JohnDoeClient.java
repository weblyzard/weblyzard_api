package com.weblyzard.api.client;

import javax.ws.rs.WebApplicationException;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
/**
 * @author sandro.hoerler@htwchur.ch
 */
public class JohnDoeClient extends BasicClient {
	private static final String PROFILE = "profileName";
	private static final String CONTENT = "content";
	private static final String BASEURL = "baseurl";
	private static final String ANNON_SERVICE_URL = "/johndoe/rest/annon";

	public JohnDoeClient() {
		super();
	}

	public JohnDoeClient(String weblyzardUrl) {
		super(weblyzardUrl);
	}
	
	/**
	 * 
	 * @param content
	 * @param profileName
	 * @return annonymized identifier
	 * @throws WebApplicationException
	 */
	public String annonymizeContent(String content, String profileName, String baseUrl) throws WebApplicationException {
		Response response = super.getTarget(ANNON_SERVICE_URL)
				.queryParam(CONTENT, content)
				.queryParam(PROFILE, profileName)
				.queryParam(BASEURL, baseUrl)
				.request(MediaType.APPLICATION_JSON).get();
		super.checkResponseStatus(response);
		String annonId = response.readEntity(String.class);
		response.close();
		return annonId;
	}
}
