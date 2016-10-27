package com.weblyzard.api;

public abstract class BasicConnector {

	protected final String weblyzard_url;
	protected final String username;
	protected final String password;

	protected static final String APPLICATIONXML = "application/xml;charset=UTF-8";
	protected static final String APPLICATIONJSON = "application/json;charset=UTF-8";

	private static final String ENV_WEBLYZARD_API_URL = "WEBLYZARD_API_URL";
	private static final String ENV_WEBLYZARD_API_USER = "WEBLYZARD_API_USER";
	private static final String ENV_WEBLYZARD_API_PASS = "WEBLYZARD_API_PASS";
	private static final String FALLBACK_WEBLYZARD_API_URL = "http://localhost:8080";



	/**
	 * Constructor using environment variables.
	 */
	public BasicConnector() {
		this(System.getenv(ENV_WEBLYZARD_API_URL));
	}



	/**
	 * Constructor using environment variables with a custom url. * @param
	 * 
	 * @param weblyzard_url
	 *            the url to the service, or FALLBACK_WEBLYZARD_API_URL if null
	 */
	public BasicConnector(String weblyzard_url) {
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
	public BasicConnector(String weblyzard_url, String username, String password) {

		if (weblyzard_url == null)
			this.weblyzard_url = FALLBACK_WEBLYZARD_API_URL;
		else
			this.weblyzard_url = weblyzard_url;

		this.username = username;
		this.password = password;
	}
}
