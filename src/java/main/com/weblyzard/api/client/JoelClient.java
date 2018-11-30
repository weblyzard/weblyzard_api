package com.weblyzard.api.client;

import java.util.Collections;
import java.util.List;
import javax.ws.rs.ClientErrorException;
import javax.ws.rs.WebApplicationException;
import javax.ws.rs.client.Entity;
import javax.ws.rs.core.GenericType;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import javax.xml.bind.JAXBException;
import com.weblyzard.api.model.document.LegacyDocument;
import com.weblyzard.api.model.joel.ClusterResult;

/**
 * Provides access to the keyword clustering service.
 * 
 * @author Philipp Kuntschik
 * @author Norman Süsstrunk
 */
public class JoelClient extends BasicClient {

    private static final String ADDDOCUMENTS_SERVICE_URL = "/rest/addDocuments";
    private static final String CLUSTER_DOCUMENT_SERVICEURL = "/rest/cluster";
    private static final String FLUSH_DOCUMENT_SERVICE_URL = "/rest/flush";

    public static final String NO_KEYWORD_IN_DOCUMENT_HEADER_MESSAGE =
            "No Keyword in Document Header";

    public JoelClient(WebserviceClientConfig c) {
        super(c, "/joel");
    }

    public Response addDocuments(List<LegacyDocument> documents)
            throws ClientErrorException, JAXBException {
        try (Response response = super.getTarget(ADDDOCUMENTS_SERVICE_URL)
                .request(MediaType.APPLICATION_JSON_TYPE).post(Entity.json(documents))) {

            super.checkResponseStatus(response);
            if (response.readEntity(String.class).equals(NO_KEYWORD_IN_DOCUMENT_HEADER_MESSAGE)) {
                throw new ClientErrorException(NO_KEYWORD_IN_DOCUMENT_HEADER_MESSAGE,
                        response.getStatus());
            }
            return response;
        }
    }

    public Response flush() throws WebApplicationException {
        try (Response response = super.getTarget(FLUSH_DOCUMENT_SERVICE_URL)
                .request(MediaType.APPLICATION_JSON_TYPE).get()) {

            super.checkResponseStatus(response);
            return response;
        }
    }

    public List<ClusterResult> cluster() throws WebApplicationException {
        try (Response response = super.getTarget(CLUSTER_DOCUMENT_SERVICEURL)
                .request(MediaType.APPLICATION_JSON_TYPE).get()) {

            super.checkResponseStatus(response);
            List<ClusterResult> clusterResults =
                    response.readEntity(new GenericType<List<ClusterResult>>() {});
            return clusterResults == null ? Collections.emptyList() : clusterResults;
        }
    }
}
