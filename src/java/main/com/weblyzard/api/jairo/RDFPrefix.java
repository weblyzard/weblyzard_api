package com.weblyzard.api.jairo;

import java.net.URI;

public class RDFPrefix {
	
	private String prefix; 
	
	private URI uri;
	
	public RDFPrefix(){}

	public RDFPrefix(String prefix, URI uri) {
		super();
		this.prefix = prefix;
		this.uri = uri;
	}

	public String getPrefix() {
		return prefix;
	}

	public void setPrefix(String prefix) {
		this.prefix = prefix;
	}

	public URI getUri() {
		return uri;
	}

	public void setUri(URI uri) {
		this.uri = uri;
	} 
}
