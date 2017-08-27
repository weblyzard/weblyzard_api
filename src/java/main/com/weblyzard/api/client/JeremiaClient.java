package com.weblyzard.api.client;

import com.weblyzard.api.model.document.Document;
import com.weblyzard.api.model.document.XmlDocument;
import javax.ws.rs.WebApplicationException;
import javax.ws.rs.client.Entity;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import javax.xml.bind.JAXBException;

/** @author philipp.kuntschik@htwchur.ch */
public class JeremiaClient extends BasicClient {

    private static final String SUBMIT_DOCUMENT_SERVICE_URL = "/jeremia/rest/submit_document";

    public JeremiaClient() {
        super();
    }

    public JeremiaClient(String weblyzardUrl) {
        super(weblyzardUrl);
    }

    public JeremiaClient(String weblyzardUrl, String username, String password) {
        super(weblyzardUrl, username, password);
    }

    public XmlDocument submitDocumentRaw(Document data) throws WebApplicationException {

        Response response =
                super.getTarget(SUBMIT_DOCUMENT_SERVICE_URL)
                        .request(MediaType.APPLICATION_JSON_TYPE)
                        .post(Entity.json(data));

        super.checkResponseStatus(response);
        XmlDocument result = response.readEntity(XmlDocument.class);
        response.close();

        return result;
    }

    public Document submitDocument(Document data) throws WebApplicationException, JAXBException {
        XmlDocument response = submitDocumentRaw(data);
        return Document.unmarshallDocumentXmlString(response.getXmlContent());
    }
}
