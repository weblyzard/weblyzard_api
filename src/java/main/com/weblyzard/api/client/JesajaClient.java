package com.weblyzard.api.client;

import com.weblyzard.api.model.document.Document;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import javax.json.JsonObject;
import javax.ws.rs.WebApplicationException;
import javax.ws.rs.client.Entity;
import javax.ws.rs.core.GenericType;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import javax.xml.bind.JAXBException;

public class JesajaClient extends BasicClient {

    private static final String TEMPLATE_MATVIEW = "matview";

    private static final String GET_KEYWORDS_SERVICE_URL =
            "/jesaja/rest/get_keywords/{" + TEMPLATE_MATVIEW + "}";
    private static final String SET_REFERENCE_CORPUS_SERVICE_URL =
            "/jesaja/rest/add_csv/{" + TEMPLATE_MATVIEW + "}";
    private static final String ADD_DOCUMENTS_SERVICE_URL =
            "/jesaja/rest/add_documents/{" + TEMPLATE_MATVIEW + "}";
    private static final String GET_NEK_ANNOTATIONS_SERVICE_URL =
            "/jesaja/rest/get_nek_annotations/{" + TEMPLATE_MATVIEW + "}";
    private static final String ROTATE_SHARD_SERVICE_URL =
            "/jesaja/rest/rotate_shard/{" + TEMPLATE_MATVIEW + "}";

    public JesajaClient() {
        super();
    }

    public JesajaClient(String weblyzardUrl) {
        super(weblyzardUrl);
    }

    public JesajaClient(String weblyzardUrl, String username, String password) {
        super(weblyzardUrl, username, password);
    }

    public Response setReferenceCorpus(String matviewId, Map<String, Integer> corpusMapping)
            throws WebApplicationException {

        Response response =
                super.getTarget(SET_REFERENCE_CORPUS_SERVICE_URL)
                        .resolveTemplate(TEMPLATE_MATVIEW, matviewId)
                        .request(MediaType.APPLICATION_JSON_TYPE)
                        .post(Entity.json(corpusMapping));

        super.checkResponseStatus(response);
        response.close();

        return response;
    }

    public Response addDocuments(String matviewId, List<Document> documents)
            throws WebApplicationException, JAXBException {

        List<String> xml = new ArrayList<>();
        for (Document document : documents) xml.add(Document.toXml(document));

        Response response =
                super.getTarget(ADD_DOCUMENTS_SERVICE_URL)
                        .resolveTemplate(TEMPLATE_MATVIEW, matviewId)
                        .request(MediaType.APPLICATION_JSON_TYPE)
                        .post(Entity.json(xml));

        super.checkResponseStatus(response);
        response.close();

        return response;
    }

    public Map<String, Map<String, Double>> getKeywords(String matviewId, List<Document> documents)
            throws WebApplicationException, JAXBException {

        List<String> xml = new ArrayList<>();
        for (Document document : documents) xml.add(Document.toXml(document));

        Response response =
                super.getTarget(GET_KEYWORDS_SERVICE_URL)
                        .resolveTemplate(TEMPLATE_MATVIEW, matviewId)
                        .request(MediaType.APPLICATION_JSON_TYPE)
                        .post(Entity.json(xml));

        super.checkResponseStatus(response);
        Map<String, Map<String, Double>> result =
                response.readEntity(new GenericType<Map<String, Map<String, Double>>>() {});
        response.close();

        return result == null ? Collections.emptyMap() : result;
    }

    public JsonObject getNonEntityKeywordAnnotations(String matviewId, List<Document> documents)
            throws WebApplicationException, JAXBException {

        List<String> xml = new ArrayList<>();
        for (Document document : documents) xml.add(Document.toXml(document));

        Response response =
                super.getTarget(GET_NEK_ANNOTATIONS_SERVICE_URL)
                        .resolveTemplate(TEMPLATE_MATVIEW, matviewId)
                        .request(MediaType.APPLICATION_JSON_TYPE)
                        .post(Entity.json(xml));

        super.checkResponseStatus(response);
        JsonObject result = response.readEntity(JsonObject.class);
        response.close();
        return result;
    }

    public int rotateShard(String matviewId) throws WebApplicationException, JAXBException {

        Response response =
                super.getTarget(ROTATE_SHARD_SERVICE_URL)
                        .resolveTemplate(TEMPLATE_MATVIEW, matviewId)
                        .request(MediaType.APPLICATION_JSON_TYPE)
                        .get();

        super.checkResponseStatus(response);
        int result = response.readEntity(Integer.class);
        response.close();
        return result;
    }
}
