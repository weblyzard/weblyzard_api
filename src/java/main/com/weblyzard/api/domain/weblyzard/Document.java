package com.weblyzard.api.domain.weblyzard;

import java.io.*;
import java.util.*;

import javax.xml.bind.JAXBContext;
import javax.xml.bind.JAXBElement;
import javax.xml.bind.JAXBException;
import javax.xml.bind.Marshaller;
import javax.xml.bind.Unmarshaller;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAnyAttribute;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.namespace.QName;

import com.weblyzard.api.i.IXMLMarshallable;

@XmlRootElement(name = "page", namespace = Document.NAMESPACE_WEBLYZARD)
@XmlAccessorType(XmlAccessType.FIELD)
public class Document implements Serializable, IXMLMarshallable<Document> {

	private final static long serialVersionUID = 1L;
	public final static String NAMESPACE_WEBLYZARD = "http://www.weblyzard.com/wl/2013#";
	public final static String NAMESPACE_DUBLIN_CORE = "http://purl.org/dc/elements/1.1/";

	@XmlAnyAttribute
	public Map<QName, String> header;

	//
	// Input only elements
	//
	@XmlElement(name = "title", namespace = Document.NAMESPACE_WEBLYZARD)
	public String title;

	@XmlElement(name = "body")
	public String body;

	// attributes required for the annotation handling
	@XmlElement(name = "body_annotation", namespace = Document.NAMESPACE_WEBLYZARD)
	private List<Annotation> bodyAnnotation;

	@XmlElement(name = "title_annotation", namespace = Document.NAMESPACE_WEBLYZARD)
	private List<Annotation> titleAnnotation;

	//
	// Elements used in the output (and input)
	//
	@XmlElement(name = "sentence", namespace = Document.NAMESPACE_WEBLYZARD)
	public List<Sentence> sentences;

	@XmlAttribute(name = "id", namespace = Document.NAMESPACE_WEBLYZARD)
	public String contentId;

	@XmlAttribute(name = "format", namespace = Document.NAMESPACE_DUBLIN_CORE)
	public String contentType;

	@XmlAttribute(name = "xml:lang")
	public String lang;

	@XmlAttribute(namespace = Document.NAMESPACE_WEBLYZARD)
	public String nilsimsa;



	// required by JAXB
	public Document() {
	}



	public Document(String body) {
		this.title = "";
		this.body = body;
	}



	public Document(String title, String body) {
		this.title = title;
		this.body = body;
	}



	public Document(String title, String content, Map<QName, String> header) {
		this.title = title;
		this.body = content;
		this.header = header;
	}



	public Document setTitle(String title) {
		this.title = title;
		return this;
	}



	public Document setBody(String body) {
		this.body = body;
		return this;
	}



	public Document setContentId(String contentId) {
		this.contentId = contentId;
		return this;
	}



	public Document setContentType(String contentType) {
		this.contentType = contentType;
		return this;
	}



	public Document setLang(String lang) {
		this.lang = lang;
		return this;
	}



	public Document setNilsimsa(String nilsimsa) {
		this.nilsimsa = nilsimsa;
		return this;
	}



	public Document setSentences(List<Sentence> sentences) {
		this.sentences = sentences;
		return this;
	}



	public Document setHeader(Map<QName, String> header) {
		this.header = header;
		return this;
	}



	public Document setTitleAnnotation(List<Annotation> titleAnnotation) {
		this.titleAnnotation = titleAnnotation;
		return this;
	}



	public Document setBodyAnnotation(List<Annotation> annotation) {
		this.bodyAnnotation = annotation;
		return this;
	}



	public List<Annotation> getTitleAnnotation() {
		return titleAnnotation != null ? titleAnnotation : Collections.<Annotation> emptyList();
	}



	public List<Annotation> getBodyAnnotation() {
		return bodyAnnotation != null ? bodyAnnotation : Collections.<Annotation> emptyList();
	}



	@Override
	public String marshal() throws JAXBException {
		StringWriter s = new StringWriter();
		JAXBElement<Document> jaxbElement = new JAXBElement<Document>(
				new QName(Document.NAMESPACE_WEBLYZARD, "page", "wl"), Document.class, this);
		JAXBContext jaxbContext = JAXBContext.newInstance(Document.class);
		Marshaller xmlMarshaller = jaxbContext.createMarshaller();
		xmlMarshaller.setProperty(Marshaller.JAXB_FORMATTED_OUTPUT, true);
		xmlMarshaller.marshal(jaxbElement, s);
		return s.toString();
	}



	@Override
	public Document unmarshal(String xml) throws JAXBException {
		JAXBContext jaxbContext = JAXBContext.newInstance(Document.class);
		Unmarshaller unmarshaller = jaxbContext.createUnmarshaller();
		StringReader reader = new StringReader(xml);
		return (Document) unmarshaller.unmarshal(reader);
	}



	@Override
	public Document unmarshal(InputStream inputStream) throws JAXBException {
		JAXBContext jaxbContext = JAXBContext.newInstance(Document.class);
		Unmarshaller unmarshaller = jaxbContext.createUnmarshaller();
		return (Document) unmarshaller.unmarshal(inputStream);
	}
}
