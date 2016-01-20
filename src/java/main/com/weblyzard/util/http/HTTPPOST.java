package com.weblyzard.util.http;

import java.io.IOException;
import java.io.InputStream;
import java.util.logging.Logger;

import org.apache.http.HttpResponse;
import org.apache.http.auth.AuthenticationException;
import org.apache.http.auth.UsernamePasswordCredentials;
import org.apache.http.client.HttpClient;
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

	private static Logger l = Logger.getLogger(HTTPPOST.class.getName());



	public static InputStream requestJSON(String url, String request, String username, String password,
			String contentType) {
		try {
			HttpClient httpClient = HttpClients.createDefault();

			HttpPost httpPost = new HttpPost(url);
			httpPost.addHeader("content-type", contentType);

			if (password != null && username != null)
				httpPost.addHeader(new BasicScheme().authenticate(new UsernamePasswordCredentials(username, password),
						httpPost, null));

			StringEntity entity = new StringEntity(request, "UTF-8");
			httpPost.setEntity(entity);

			HttpResponse httpResponse = httpClient.execute(httpPost);

			return httpResponse	.getEntity()
								.getContent();

		} catch (IOException | AuthenticationException e) {
			l.warning("Could not finish POST-Request for [url: " + url + " ; Entity: " + request
					+ " ; contentType: " + contentType + "]");
			e.printStackTrace();
		}
		return null;
	}
}