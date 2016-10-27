package com.weblyzard.api.document_api;

public class Metadata {

	public String author;
	public String published_date;



	public Metadata() {
	}



	public Metadata setAuthor(String author) {
		this.author = author;
		return this;
	}



	public Metadata setPublished_date(String published_date) {
		this.published_date = published_date;
		return this;
	}



	public Metadata(String author, String published_date) {
		super();
		this.author = author;
		this.published_date = published_date;
	}

}
