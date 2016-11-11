package com.weblyzard.api.joel;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;
import com.weblyzard.api.document.Document;

/**
 * 
 * @author norman.suesstrunk@htwchur.ch
 * @author albert.weichselbraun@htwchur.ch
 *
 */

public class KeywordDocument implements Serializable {

	private static final long serialVersionUID = 1L;
	
	public final static String FIELD_KEYWORDS = "tokens";
	public final static String FIELD_SENTENCES = "sentences";
	
	private Document document; 
	
	private List<String> keywords; 
	
	public KeywordDocument() {}
	
	public KeywordDocument(Document document) {
		this.document = document; 
		initKeywordsFromDocument(); 
	}

	private void initKeywordsFromDocument() {
		if (document.getHeader() != null) {
			this.keywords = Arrays
					.asList(document.getHeader().get(com.weblyzard.api.document.Document.WL_KEYWORD_ATTR).split(";"))
					.stream().map(s -> s.trim()).collect(Collectors.toList());

		} else {
			this.keywords = new ArrayList<>();
		}
	}
	
	public void setKeywords(List<String> keywords) {
		this.keywords = keywords; 
	}

	public List<String> getKeywords() {
		return keywords;
	}

	public Document getDocument() {
		return document; 
	}
}
