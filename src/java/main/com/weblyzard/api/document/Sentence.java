package com.weblyzard.api.document;

import java.io.Serializable;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.XmlValue;
import javax.xml.bind.annotation.adapters.XmlJavaTypeAdapter;

import org.eclipse.persistence.oxm.annotations.XmlCDATA;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.weblyzard.api.datatype.MD5Digest;
import com.weblyzard.api.document.serialize.xml.BooleanAdapter;

/**
 * 
 * webLyzard Sentence class 
 * @author: Albert Weichselbraun <weichselbraun@weblyzard.com>
 * 
 **/
@XmlAccessorType(XmlAccessType.FIELD)
public class Sentence implements Serializable {
	private static final long serialVersionUID = 1L;

	@XmlAttribute(name="id", namespace=Document.NS_WEBLYZARD)
	@XmlJavaTypeAdapter(MD5Digest.class)
	private MD5Digest id;

	/**
	 * The POS dependency tree of the given sentence.
	 */
	@XmlAttribute(name="pos", namespace=Document.NS_WEBLYZARD)
	private String pos;	
	
	@XmlAttribute(name="dependency", namespace=Document.NS_WEBLYZARD)
	private String dependency;
	
	@XmlAttribute(name="token", namespace=Document.NS_WEBLYZARD)
	private String token;
	
	@JsonProperty("is_title")
	@XmlAttribute(name="is_title", namespace=Document.NS_WEBLYZARD)
	@XmlJavaTypeAdapter(BooleanAdapter.class)
	private boolean isTitle;

	@JsonProperty("text")
	@XmlValue 
	@XmlCDATA
	private String text;
	
	// additional attributes defined in the weblyzard XML format
	@JsonProperty("sem_orient")
	@XmlAttribute(name="sem_orient", namespace=Document.NS_WEBLYZARD)
	private double semOrient;
	
	@XmlAttribute(name="significance", namespace=Document.NS_WEBLYZARD)
	private double significance;	


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
	
	public String getText() { 
		return text; 
	}

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
		
	public String toString() {
		return text;
	}

	public MD5Digest getId() {
		return id;
	}

	public void setId(MD5Digest id) {
		this.id = id;
	}

	public boolean isIs_title() {
		return isTitle;
	}
	
	public void setIs_title(boolean isTitle) {
		this.isTitle = isTitle;
	}

	public double getSem_orient() {
		return semOrient;
	}

	public void setSem_orient(double sem_orient) {
		this.semOrient = sem_orient;
	}

	public double getSignificance() {
		return significance;
	}

	public void setSignificance(double significance) {
		this.significance = significance;
	}

	public String getDependency() {
		return dependency;
	}

	public void setDependency(String dependency) {
		this.dependency = dependency;
	}

	public void setToken(String token) {
		this.token = token;
	}

}
