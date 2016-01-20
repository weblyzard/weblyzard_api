package com.weblyzard.api.domain.weblyzard;

/**************************************************************************
 * 
 * webLyzard Sentence class 
 * @author: Albert Weichselbraun <weichselbraun@weblyzard.com>
 * 
 **************************************************************************/

import java.io.Serializable;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.XmlValue;

import org.eclipse.persistence.oxm.annotations.XmlCDATA;

@XmlAccessorType(XmlAccessType.FIELD)
public class Sentence implements Serializable {

	private static final long serialVersionUID = 1L;

	@XmlAttribute(name = "id", namespace = Document.NAMESPACE_WEBLYZARD)
	public String md5sum;

	/**
	 * The POS dependency tree of the given sentence.
	 */
	@XmlAttribute(name = "pos", namespace = Document.NAMESPACE_WEBLYZARD)
	public String pos;

	@XmlAttribute(name = "dependency", namespace = Document.NAMESPACE_WEBLYZARD)
	public String dependency;

	@XmlAttribute(name = "token", namespace = Document.NAMESPACE_WEBLYZARD)
	public String token;

	@XmlAttribute(name = "is_title", namespace = Document.NAMESPACE_WEBLYZARD)
	public boolean isTitle;

	@XmlValue
	@XmlCDATA
	public String text;

	// additional attributes defined in the weblyzard XML format
	@XmlAttribute(name = "sem_orient", namespace = Document.NAMESPACE_WEBLYZARD)
	public double sentimentPolartiy;

	@XmlAttribute(name = "significance", namespace = Document.NAMESPACE_WEBLYZARD)
	public double significance;



	// required by JAXB
	public Sentence() {
	}



	public Sentence(String text) {
		this.text = text;
	}



	public Sentence(String text, String token, String pos) {
		this(text);
		this.token = token;
		this.pos = pos;
	}



	public Sentence(String text, String token, String pos, String dependency) {
		this(text, token, pos);
		this.dependency = dependency;
	}



	public Sentence setText(String text) {
		// required to allow marshalling of the XML document (!)
		this.text = text.replace("\"", "&quot;");
		return this;
	}



	public Sentence setPos(String pos) {
		// required for handling double quotes in POS tags.
		this.pos = pos.replace("\"", "&quot;");
		return this;
	}



	public Sentence setToken(String token) {
		this.token = token;
		return this;
	}



	public Sentence setTitle(boolean isTitle) {
		this.isTitle = isTitle;
		return this;
	}



	public Sentence setSignificance(double significance) {
		this.significance = significance;
		return this;
	}



	public Sentence setSentimentPolartiy(double sentimentPolartiy) {
		this.sentimentPolartiy = sentimentPolartiy;
		return this;
	}



	public Sentence setMd5sum(String md5sum) {
		this.md5sum = md5sum;
		return this;
	}



	public Sentence setDependency(String dependency) {
		this.dependency = dependency;
		return this;
	}



	public String toString() {
		return text;
	}

}
