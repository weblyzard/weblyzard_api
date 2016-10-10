package com.weblyzard.api;

import java.io.IOException;
import java.io.InputStream;
import java.util.List;

import org.apache.http.auth.AuthenticationException;
import org.apache.http.client.ClientProtocolException;

import com.google.gson.reflect.TypeToken;
import com.weblyzard.api.domain.weblyzard.Annotation;
import com.weblyzard.util.GSONHelper;
import com.weblyzard.util.http.HTTPPOST;

public class JairoConnector extends BasicConnector

{

	private static final String EXTEND_ANNOTATIONS = "/jairo/extend_annotations/";



	/**
	 * @see BasicConnector
	 */
	public JairoConnector() {
		super();
	}



	/**
	 * @see BasicConnector
	 */
	public JairoConnector(String weblyzard_url) {
		super(weblyzard_url);
	}



	/**
	 * @see BasicConnector
	 */
	public JairoConnector(String weblyzard_url, String username, String password) {
		super(weblyzard_url, username, password);
	}



	public List<Annotation> call_extendAnnotations(String profileName, List<Annotation> annotations)
			throws AuthenticationException, ClientProtocolException, IOException {
		
		String url = super.weblyzard_url + EXTEND_ANNOTATIONS + profileName;

		InputStream responseStream = HTTPPOST.requestJSON(url,
				GSONHelper.parseObject(annotations, new TypeToken<List<Annotation>>(){}.getType()), 
				super.username,	super.password, APPLICATIONJSON);

		return (List<Annotation>) GSONHelper.parseInputStream(responseStream, new TypeToken<List<Annotation>>(){}.getType());
	}
}
