package com.weblyzard.api.client;

import javax.ws.rs.ClientErrorException;
import javax.ws.rs.client.Entity;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;

import com.weblyzard.api.document.Document;
import com.weblyzard.api.domain.weblyzard.XmlDocument;

/**
 * 
 * @author philipp.kuntschik@htwchur.ch
 *
 */
public class JeremiaClient extends BasicClient {

	private static final String SUBMITDOCUMENTSERVICEURL = "/jeremia/rest/submit_document";



	/**
	 * @see BasicClient
	 */
	public JeremiaClient() {
		super();
	}



	/**
	 * @see BasicClient
	 */
	public JeremiaClient(String weblyzard_url) {
		super(weblyzard_url);
	}



	/**
	 * @see BasicClient
	 */
	public JeremiaClient(String weblyzard_url, String username, String password) {
		super(weblyzard_url, username, password);
	}



	public XmlDocument submitDocumentRaw(Document data) throws ClientErrorException {

		Response response = super.target.path(SUBMITDOCUMENTSERVICEURL).request(MediaType.APPLICATION_JSON_TYPE)
				.post(Entity.json(data));

		super.checkResponseStatus(response);
		XmlDocument result = response.readEntity(XmlDocument.class);
		response.close();

		return result;
	}



	public Document submitDocument(Document data) throws ClientErrorException {
		XmlDocument response = submitDocumentRaw(data);
		return Document.unmarshallDocumentXMLString(response.xml_content);
	}
}
