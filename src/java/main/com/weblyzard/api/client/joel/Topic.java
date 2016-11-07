package com.weblyzard.api.client.joel;

import java.io.Serializable;
import java.util.List;

/**
 * 
 * @author Norman Suesstrunk
 * 
 * A Topic is characterized by its "title" and a list of keywords that
 * frequently occur in documents covering the topic.
 * 
 * Keywords are represented by their corresponding URLs
 *
 */
public class Topic implements Serializable{
	
	private static final long serialVersionUID = 1L;

	private String title; 
	
	private List<String> contextKeywords;
	
	public Topic() {}
	
	public Topic(String title, List<String> contextKeywords) {
		super();
		this.title = title;
		this.contextKeywords = contextKeywords;
	}
	
	public Topic(String title) {
		super();
		this.title = title;
		
	}

	public String getTitle() {
		return title;
	}

	public void setTitle(String title) {
		this.title = title;
	}

	/**
	 * @return
	 * 	a list of identifiers (URLs) for the context keywords
	 */
	public List<String> getContextKeywords() {
		return contextKeywords;
	}

	public void setContextKeywords(List<String> contextKeywords) {
		this.contextKeywords = contextKeywords;
	} 	
}
