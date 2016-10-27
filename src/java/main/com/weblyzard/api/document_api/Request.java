package com.weblyzard.api.document_api;

public class Request {

	public String repository_id;
	public String title;
	public String uri;
	public String content;
	public String content_type;
	public Metadata meta_data;



	public Request() {
	}



	public Request setUri(String uri) {
		this.uri = uri;
		return this;
	}



	public Request setTitle(String title) {
		this.title = title;
		return this;
	}



	public Request setRepository_id(String repository_id) {
		this.repository_id = repository_id;
		return this;
	}



	public Request setMeta_data(Metadata meta_data) {
		this.meta_data = meta_data;
		return this;
	}



	public Request setContent_type(String content_type) {
		this.content_type = content_type;
		return this;
	}



	public Request setContent(String content) {
		this.content = content;
		return this;
	}
}
