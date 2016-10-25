package com.weblyzard.lib.document;

/**************************************************************************
 * 
 * webLyzard Sentence class 
 * @author: Albert Weichselbraun <weichselbraun@weblyzard.com>
 * 
 **************************************************************************/


import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;
import java.util.logging.Logger;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.XmlValue;
import javax.xml.bind.annotation.adapters.XmlJavaTypeAdapter;

import org.eclipse.persistence.oxm.annotations.XmlCDATA;


import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.google.common.base.Splitter;
import com.weblyzard.lib.MD5Digest;

@XmlAccessorType(XmlAccessType.FIELD)
public class Sentence implements Serializable {
	private static final long serialVersionUID = 1L;

	
	public final static Logger logger = Logger.getLogger(Sentence.class.getName());
	private static final Splitter WHITE_SPACE_SPLITTER = Splitter.on(" ");
	

	@XmlAttribute(name="id", namespace=Document.NS_WEBLYZARD)
	@XmlJavaTypeAdapter(MD5Digest.class)
	public MD5Digest id;

	/**
	 * The POS dependency tree of the given sentence.
	 */
	@XmlAttribute(name="pos", namespace=Document.NS_WEBLYZARD)
	private String pos;	
	
	@XmlAttribute(name="dependency", namespace=Document.NS_WEBLYZARD)
	public String dependency;
	
	@XmlAttribute(name="token", namespace=Document.NS_WEBLYZARD)
	public String token;
	
	@XmlAttribute(name="is_title", namespace=Document.NS_WEBLYZARD)
	@XmlJavaTypeAdapter(BooleanAdapter.class)
	public boolean is_title;

	@XmlValue 
	@XmlCDATA
	public String text;
	
	// additional attributes defined in the weblyzard XML format
	@XmlAttribute(name="sem_orient", namespace=Document.NS_WEBLYZARD)
	public double sem_orient;
	
	@XmlAttribute(name="significance", namespace=Document.NS_WEBLYZARD)
	public double significance;	


	// required by JAXB
	public Sentence() {}
	
	public Sentence(String text)  {
		this.text = text;
		id = MD5Digest.fromText(text);
	}
	
	
	public Sentence (String text, String token, String pos) {
		this(text);
		this.token = token;
		this.pos   = pos;
	}
	
	public Sentence(String text, String token, String pos, String dependency) {
		this(text, token, pos);
		this.dependency = dependency;
	}
	
	@JsonProperty("text")
	public String getText() { 
		return text; 
	}

	@JsonProperty("text")
	public void setText(String text) {
		// required to allow marshalling of the XML document (!)
		this.text = text.replace("\"", "&quot;");
	}
	
	public void setPos(String pos) {
		// required for handling double quotes in POS tags.
		this.pos = pos.replace("\"", "&quot;");
	}

	public String getPos() { 
		return pos; 
	}
	
	public String getToken() { 
		return token; 
	}
		
	/**
	 * @return
	 * 		a list of tokens for the given sentence.
	 */
	@JsonIgnore
	public List<String> getTokenList() {
		List<String> result = new ArrayList<>();
		int separatorPos;
		try {
			for (String tokenPos: WHITE_SPACE_SPLITTER.split(token)) {
				separatorPos = tokenPos.indexOf(',');
				result.add(text.substring(Integer.parseInt(tokenPos.substring(0, separatorPos)), 
						Integer.parseInt(tokenPos.substring(separatorPos+1))));
			} 
		} 
		catch (StringIndexOutOfBoundsException e) {
			logger.warning(String.format("Invalid tokenization for sentence '%s' with tokens '%s' (%s).", 
					getText(), getPos(), e));
		}
		return result;
	}
	
	
	/**
	 * @return
	 * 		a list of pos tags for the given sentence.
	 */
	@JsonIgnore
	public List<String> getPosList() {
		return WHITE_SPACE_SPLITTER.splitToList(pos);
	}
			
	public String toString() {
		return text;
	}
}
