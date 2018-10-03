package com.weblyzard.api.client;

import javax.ws.rs.WebApplicationException;
import javax.ws.rs.client.Entity;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;

public class InscriptisClient extends BasicClient {

    private static final String GET_TEXT = "get_text";


    public InscriptisClient(WebserviceClientConfig c) {
        super(c);
        c.setServicePrefixIfEmpty("");
    }

    public String parseHTMl(String html) throws WebApplicationException {
        Response response =
                super.getTarget(GET_TEXT).request(MediaType.TEXT_HTML).post(Entity.text(html));
        super.checkResponseStatus(response);
        String parseResult = response.readEntity(String.class);
        response.close();
        return parseResult;
    }

}
