package com.weblyzard.util.http;

import java.io.IOException;
import java.io.InputStream;


import org.apache.http.HttpResponse;
import org.apache.http.auth.AuthenticationException;
import org.apache.http.auth.UsernamePasswordCredentials;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.HttpResponseException;
import org.apache.http.client.methods.HttpPut;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.auth.BasicScheme;
import org.apache.http.impl.client.HttpClients;

public class HTTPPUT {

	/**
	 * 
	 * @param url
	 *            the called service-url
	 * @param request
	 *            the request that gets sent to the service-url
	 * @param username
	 *            basicauthentication username, may be null
	 * @param password
	 *            basicauthentication username, may be null
	 * @param contentType
	 *            supported contentTypes are "application/json" and
	 *            "application/xml". A target charset can be specified separated
	 *            by semicolon, like "application/json;charset=UTF-8"
	 * @return
	 * @throws AuthenticationException
	 * @throws ClientProtocolException
	 * @throws IOException
	 */
	public static InputStream requestContent(String url, String request, String username, String password,
			String contentType) throws AuthenticationException, ClientProtocolException, IOException {
		HttpResponse httpResponse = requestResponse(url, request, username, password, contentType);

		switch (httpResponse.getStatusLine()
							.getStatusCode()) {
		case 500:
			throw new HttpResponseException(500, "internal server error for url: " + url);
		default:
			return httpResponse	.getEntity()
								.getContent();
		}
	}



	/**
	 * 
	 * @param url
	 *            the called service-url
	 * @param request
	 *            the request that gets sent to the service-url
	 * @param username
	 *            basicauthentication username, may be null
	 * @param password
	 *            basicauthentication username, may be null
	 * @param contentType
	 *            supported contentTypes are "application/json" and
	 *            "application/xml". A target charset can be specified separated
	 *            by semicolon, like "application/json;charset=UTF-8"
	 * @return
	 * @throws AuthenticationException
	 * @throws ClientProtocolException
	 * @throws IOException
	 */
	public static HttpResponse requestResponse(String url, String request, String username, String password,
			String contentType) throws AuthenticationException, ClientProtocolException, IOException {

		HttpClient httpClient = HttpClients.createDefault();
		HttpPut httpPut = new HttpPut(url);

		httpPut.addHeader("content-type", contentType);
		if (password != null && username != null)
			httpPut.addHeader(
					new BasicScheme().authenticate(new UsernamePasswordCredentials(username, password), httpPut, null));

		StringEntity entity = new StringEntity(request, "UTF-8");
		httpPut.setEntity(entity);

		return httpClient.execute(httpPut);
	}
}
