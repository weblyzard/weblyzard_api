package com.weblyzard.api.client;

import javax.ws.rs.client.ClientBuilder;
import javax.ws.rs.client.WebTarget;

import org.glassfish.jersey.client.ClientConfig;
import org.glassfish.jersey.client.authentication.HttpAuthenticationFeature;

public abstract class BasicClient {

	private static final String ENV_WEBLYZARD_API_URL = "WEBLYZARD_API_URL";
	private static final String ENV_WEBLYZARD_API_USER = "WEBLYZARD_API_USER";
	private static final String ENV_WEBLYZARD_API_PASS = "WEBLYZARD_API_PASS";
	private static final String FALLBACK_WEBLYZARD_API_URL = "http://localhost:8080";

	protected WebTarget target;



	/**
	 * Constructor using environment variables.
	 */
	public BasicClient() {
		this(System.getenv(ENV_WEBLYZARD_API_URL));
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
		if (username != null && password != null)
			config.register(HttpAuthenticationFeature.basicBuilder()
						.nonPreemptive()
						.credentials(username, password)
						.build());

		this.target = ClientBuilder.newClient(config)
				.target(weblyzard_url == null ? 
						FALLBACK_WEBLYZARD_API_URL : weblyzard_url);
	}
}
