package com.weblyzard.api.client;

import javax.ws.rs.ClientErrorException;
import javax.ws.rs.client.Entity;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import javax.xml.bind.JAXBException;

import com.weblyzard.api.document.Document;
import com.weblyzard.api.document.XmlDocument;

/**
 * 
 * @author philipp.kuntschik@htwchur.ch
 *
 */
public class JeremiaClient extends BasicClient {

	private static final String SUBMIT_DOCUMENT_SERVICE_URL = "/jeremia/rest/submit_document";


	public JeremiaClient() {
		super();
	}

	public JeremiaClient(String weblyzard_url) {
		super(weblyzard_url);
	}

	public JeremiaClient(String weblyzard_url, String username, String password) {
		super(weblyzard_url, username, password);
	}

	public XmlDocument submitDocumentRaw(Document data) throws ClientErrorException {

		Response response = super.target.path(SUBMIT_DOCUMENT_SERVICE_URL).request(MediaType.APPLICATION_JSON_TYPE)
				.post(Entity.json(data));

		super.checkResponseStatus(response);
		XmlDocument result = response.readEntity(XmlDocument.class);
		response.close();

		return result;
	}



	public Document submitDocument(Document data) throws ClientErrorException, JAXBException {
		XmlDocument response = submitDocumentRaw(data);
		return Document.unmarshallDocumentXmlString(response.xml_content);
	}
}
