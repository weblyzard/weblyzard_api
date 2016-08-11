package com.weblyzard.util.http;

import java.io.IOException;
import java.io.InputStream;

import org.apache.http.HttpResponse;
import org.apache.http.auth.AuthenticationException;
import org.apache.http.auth.UsernamePasswordCredentials;
import org.apache.http.client.HttpClient;
import org.apache.http.client.HttpResponseException;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.auth.BasicScheme;
import org.apache.http.impl.client.HttpClients;

/**
 * 
 * @author philipp.kuntschik@htwchur.ch
 *
 */
public class HTTPGET {

	public static InputStream requestJSON(String url, String username, String password, String contentType)
			throws IllegalStateException, IOException, AuthenticationException {

		HttpClient httpClient = HttpClients.createDefault();
		HttpGet httpGet = new HttpGet(url);

		httpGet.addHeader("content-type", contentType);

		// TODO: if authentication fails, should the request still be executed?
		if (password != null && username != null)
			httpGet.addHeader(
					new BasicScheme().authenticate(new UsernamePasswordCredentials(username, password), httpGet, null));

		HttpResponse httpResponse = httpClient.execute(httpGet);

		switch (httpResponse.getStatusLine()
							.getStatusCode()) {
		case 400:
			throw new HttpResponseException(400, "bad request for url: " + url);
		case 401:
			throw new HttpResponseException(401, "unauthorized for url: " + url);
		case 500:
			throw new HttpResponseException(500, "internal server error for url: " + url);
		default:
			return httpResponse	.getEntity()
								.getContent();
		}
	}
}
