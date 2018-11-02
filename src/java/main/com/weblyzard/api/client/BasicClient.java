package com.weblyzard.api.client;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.ws.rs.BadRequestException;
import javax.ws.rs.InternalServerErrorException;
import javax.ws.rs.NotAllowedException;
import javax.ws.rs.NotAuthorizedException;
import javax.ws.rs.NotFoundException;
import javax.ws.rs.WebApplicationException;
import javax.ws.rs.client.WebTarget;
import javax.ws.rs.core.Response;
import org.glassfish.jersey.client.ClientConfig;
import org.glassfish.jersey.client.ClientProperties;
import org.glassfish.jersey.client.JerseyClientBuilder;
import org.glassfish.jersey.client.authentication.HttpAuthenticationFeature;
import org.glassfish.jersey.client.filter.EncodingFilter;
import org.glassfish.jersey.jackson.internal.jackson.jaxrs.json.JacksonJsonProvider;
import org.glassfish.jersey.logging.LoggingFeature;
import org.glassfish.jersey.message.GZipEncoder;

public abstract class BasicClient {

    private final WebTarget baseTarget;
    private Map<String, WebTarget> webTargets = new ConcurrentHashMap<>();

    private Logger logger = Logger.getLogger(getClass().getName());


    /**
     * Constructs the {@link BasicClient} based on a {@link WebserviceClientConfig}
     * 
     * @param c the {@link WebserviceClientConfig} to use for the connection
     * @param defaultServicePrefix the default Web service prefix for the given component
     */
    public BasicClient(WebserviceClientConfig c, String defaultServicePrefix) {
        baseTarget = getClient(c, defaultServicePrefix, false);
        if (c.isDebug()) {
            // https://jersey.java.net/documentation/latest/user-guide.html#logging_chapter
            // -> Example 21.1. Logging on client-side
            baseTarget.register(new LoggingFeature(logger, Level.SEVERE,
                    LoggingFeature.Verbosity.PAYLOAD_TEXT, LoggingFeature.DEFAULT_MAX_ENTITY_SIZE));
        }
    }

    public static WebTarget getClient(WebserviceClientConfig c, String defaultServicePrefix, boolean enableCompression) {
        ClientConfig config = new ClientConfig();

        if (enableCompression) {
            config.register(EncodingFilter.class)
            .register(GZipEncoder.class)
            .property(ClientProperties.USE_ENCODING, "gzip");
        }

        if (c.getUsername() != null && c.getPassword() != null) {
            config.register(HttpAuthenticationFeature.basicBuilder()
                    .credentials(c.getUsername(), c.getPassword()).build());
        }

        return JerseyClientBuilder.createClient(config)
                .target(c.getUrl() + c.getServicePrefix(defaultServicePrefix))
                .register(new JacksonJsonProvider());
    }

    public WebTarget getTarget(String urlTemplate) {
        this.webTargets.putIfAbsent(urlTemplate, this.baseTarget.path(urlTemplate));
        return this.webTargets.get(urlTemplate);
    }

    public WebTarget getBaseTarget() {
        return this.baseTarget;
    }

    public void checkResponseStatus(Response response) throws WebApplicationException {
        switch (response.getStatus()) {
            case 200:
                return;
            case 204:
                return;
            case 400:
                throw new BadRequestException(response);
            case 401:
                throw new NotAuthorizedException(response);
            case 404:
                throw new NotFoundException(response);
            case 405:
                throw new NotAllowedException(response);
            case 500:
                throw new InternalServerErrorException(response);
            default:
                throw new WebApplicationException(response);
        }
    }
}
