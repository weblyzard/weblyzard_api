package com.weblyzard.api.client;

import java.util.logging.Level;
import java.util.logging.Logger;

import javax.ws.rs.BadRequestException;
import javax.ws.rs.InternalServerErrorException;
import javax.ws.rs.NotAllowedException;
import javax.ws.rs.NotAuthorizedException;
import javax.ws.rs.NotFoundException;
import javax.ws.rs.WebApplicationException;
import javax.ws.rs.client.ClientBuilder;
import javax.ws.rs.client.WebTarget;
import javax.ws.rs.core.Response;

import org.glassfish.jersey.client.ClientConfig;
import org.glassfish.jersey.client.authentication.HttpAuthenticationFeature;
import org.glassfish.jersey.logging.LoggingFeature;

public abstract class BasicClient {

	private static final String ENV_WEBLYZARD_API_URL = "WEBLYZARD_API_URL";
	private static final String ENV_WEBLYZARD_API_USER = "WEBLYZARD_API_USER";
	private static final String ENV_WEBLYZARD_API_PASS = "WEBLYZARD_API_PASS";
	private static final String FALLBACK_WEBLYZARD_API_URL = "http://localhost:8080";

	private static final String ENV_WEBLYZARD_API_DEBUG = "WEBLYZARD_API_DEBUG";

	protected WebTarget target;

	private Logger logger = Logger.getLogger(getClass().getName());



	/**
	 * Constructor using environment variables.
	 */
	public BasicClient() {
		this(System.getenv(ENV_WEBLYZARD_API_URL));
		ClientBuilder.newClient();
	}



	/**
	 * Constructor using environment variables with a custom url.
	 * 
	 * @param weblyzard_url
	 *            the url to the service, or FALLBACK_WEBLYZARD_API_URL if null
	 */
	public BasicClient(String weblyzard_url) {
		this(weblyzard_url, System.getenv(ENV_WEBLYZARD_API_USER), System.getenv(ENV_WEBLYZARD_API_PASS));
	}



	/**
	 * Constructor using a custom url, username and password.
	 * 
	 * @param weblyzard_url
	 *            the url to the service, or FALLBACK_WEBLYZARD_API_URL if null
	 * @param username
	 *            may be null
	 * @param password
	 *            may be null
	 */
	public BasicClient(String weblyzard_url, String username, String password) {

		ClientConfig config = new ClientConfig();

		if(!Boolean.parseBoolean(System.getenv(ENV_WEBLYZARD_API_DEBUG))){
			// https://jersey.java.net/documentation/latest/user-guide.html#logging_chapter
			// -> Example 21.1. Logging on client-side
			config.register(new LoggingFeature(logger, Level.SEVERE, LoggingFeature.Verbosity.PAYLOAD_TEXT,
					LoggingFeature.DEFAULT_MAX_ENTITY_SIZE));
		}

		if (username != null && password != null) {
			config.register(
					HttpAuthenticationFeature.basicBuilder().nonPreemptive().credentials(username, password).build());
		}

		this.target = ClientBuilder.newClient(config)
				.target(weblyzard_url == null ? FALLBACK_WEBLYZARD_API_URL : weblyzard_url);
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
