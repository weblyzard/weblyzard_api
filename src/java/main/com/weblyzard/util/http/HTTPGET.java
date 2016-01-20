package com.weblyzard.util.http;

import java.io.IOException;
import java.io.InputStream;
import java.util.logging.Logger;

import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.HttpClients;

/**
 * 
 * @author philipp.kuntschik@htwchur.ch
 *
 */
public class HTTPGET {

	private static Logger l = Logger.getLogger(HTTPGET.class.getName());



	public static InputStream requestJSON(String loadRecognizeURL) {
		try {
			HttpClient httpClient = HttpClients.createDefault();

			HttpGet httpGet = new HttpGet(loadRecognizeURL);

			HttpResponse httpResponse = httpClient.execute(httpGet);

			return httpResponse	.getEntity()
								.getContent();

		} catch (IOException e) {
			l.warning("Could not finish POST-Request for [url: " + loadRecognizeURL + "]");
			e.printStackTrace();
		}

		return null;
	}

}
