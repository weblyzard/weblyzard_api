package com.weblyzard.util.http;

import java.io.IOException;
import java.io.InputStream;

import org.apache.http.HttpResponse;
import org.apache.http.auth.AuthenticationException;
import org.apache.http.auth.UsernamePasswordCredentials;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.HttpResponseException;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.auth.BasicScheme;
import org.apache.http.impl.client.HttpClients;

/**
 * 
 * @author philipp.kuntschik@htwchur.ch
 *
 */
public class HTTPPOST {

	public static InputStream requestJSON(String url, String request, String username, String password,
			String contentType) throws AuthenticationException, ClientProtocolException, IOException {

		HttpClient httpClient = HttpClients.createDefault();
		HttpPost httpPost = new HttpPost(url);

		httpPost.addHeader("content-type", contentType);
		if (password != null && username != null)
			httpPost.addHeader(new BasicScheme().authenticate(new UsernamePasswordCredentials(username, password),
					httpPost, null));

		StringEntity entity = new StringEntity(request, "UTF-8");
		httpPost.setEntity(entity);

		HttpResponse httpResponse = httpClient.execute(httpPost);

		switch (httpResponse.getStatusLine().getStatusCode()) {
		case 400:
			throw new HttpResponseException(400,
					"'" + httpResponse.getStatusLine().getReasonPhrase() + "' for url: " + url);
		case 401:
			throw new HttpResponseException(401,
					"'" + httpResponse.getStatusLine().getReasonPhrase() + "' for url: " + url);
		case 404:
			throw new HttpResponseException(404,
					"'" + httpResponse.getStatusLine().getReasonPhrase() + "' for url: " + url);
		case 500:
			throw new HttpResponseException(500,
					"'" + httpResponse.getStatusLine().getReasonPhrase() + "' for url: " + url);
		default:
			return httpResponse.getEntity().getContent();
		}
	}
}