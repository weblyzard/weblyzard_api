package com.weblyzard.api.client;

import com.weblyzard.api.model.document.Document;
import com.weblyzard.api.model.joel.ClusterResult;
import java.util.Collections;
import java.util.List;
import javax.ws.rs.ClientErrorException;
import javax.ws.rs.WebApplicationException;
import javax.ws.rs.client.Entity;
import javax.ws.rs.core.GenericType;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import javax.xml.bind.JAXBException;

/**
 * @author philipp.kuntschik@htwchur.ch
 * @author norman.suesstrunk@htwchur.ch
 */
public class JoelClient extends BasicClient {

    private static final String ADDDOCUMENTS_SERVICE_URL = "/joel/rest/addDocuments";
    private static final String CLUSTER_DOCUMENT_SERVICEURL = "/joel/rest/cluster";
    private static final String FLUSH_DOCUMENT_SERVICE_URL = "/joel/rest/flush";

    public static final String NO_KEYWORD_IN_DOCUMENT_HEADER_MESSAGE =
            "No Keyword in Document Header";

    public JoelClient() {
        super();
    }

    public JoelClient(String weblyzardUrl) {
        super(weblyzardUrl);
    }

    public JoelClient(String weblyzardUrl, String username, String password) {
        super(weblyzardUrl, username, password);
    }

    public Response addDocuments(List<Document> documents)
            throws ClientErrorException, JAXBException {
        Response response =
                super.getTarget(ADDDOCUMENTS_SERVICE_URL)
                        .request(MediaType.APPLICATION_JSON_TYPE)
                        .post(Entity.json(documents));

        super.checkResponseStatus(response);
        if (response.readEntity(String.class).equals(NO_KEYWORD_IN_DOCUMENT_HEADER_MESSAGE)) {
            throw new ClientErrorException(
                    NO_KEYWORD_IN_DOCUMENT_HEADER_MESSAGE, response.getStatus());
        }
        response.close();
        return response;
    }

    public Response flush() throws WebApplicationException {
        Response response =
                super.getTarget(FLUSH_DOCUMENT_SERVICE_URL)
                        .request(MediaType.APPLICATION_JSON_TYPE)
                        .get();

        super.checkResponseStatus(response);
        response.close();
        return response;
    }

    public List<ClusterResult> cluster() throws WebApplicationException {
        Response response =
                super.getTarget(CLUSTER_DOCUMENT_SERVICEURL)
                        .request(MediaType.APPLICATION_JSON_TYPE)
                        .get();

        super.checkResponseStatus(response);
        List<ClusterResult> clusterResults =
                response.readEntity(new GenericType<List<ClusterResult>>() {});
        response.close();
        return clusterResults == null ? Collections.emptyList() : clusterResults;
    }
}
