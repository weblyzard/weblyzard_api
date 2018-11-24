package com.weblyzard.api.client;

import javax.ws.rs.client.Entity;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;

/**
 * HTML to text Web service
 * 
 * @author Albert Weichselbraun
 *
 */
public class InscriptisClient extends BasicClient {

    private static final String GET_TEXT = "/get_text";


    public InscriptisClient(WebserviceClientConfig c) {
        super(c, "/inscriptis");
    }

    /**
     * Provides a text representation of an HTML file.
     * 
     * @param html the HTML source code
     * @return the corresponding text representation
     */
    public String parseHtml(String html) {
        try (Response response =
                super.getTarget(GET_TEXT).request(MediaType.TEXT_HTML).post(Entity.text(html))) {
            super.checkResponseStatus(response);
            String parseResult = response.readEntity(String.class);
            return parseResult;
        }
    }

}
