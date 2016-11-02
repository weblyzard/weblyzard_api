package com.weblyzard.api.document;

import java.io.Serializable;
import java.io.StringReader;
import java.io.StringWriter;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

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

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import com.fasterxml.jackson.databind.annotation.JsonSerialize;
import com.weblyzard.api.document.annotation.Annotation;
import com.weblyzard.api.document.serialize.json.DocumentHeaderDeserializer;
import com.weblyzard.api.document.serialize.json.DocumentHeaderSerializer;

@XmlRootElement(name="page", namespace=Document.NS_WEBLYZARD)
@JsonIgnoreProperties(ignoreUnknown = true)
@XmlAccessorType(XmlAccessType.FIELD)
public class Document implements Serializable {
	
	private final static long serialVersionUID = 1L;
	public final static String NS_WEBLYZARD = "http://www.weblyzard.com/wl/2013#";
	public final static String NS_DUBLIN_CORE = "http://purl.org/dc/elements/1.1/";

	public final static QName WL_KEYWORD_ATTR = new QName(NS_DUBLIN_CORE, "subject");
	
	@JsonDeserialize	(keyUsing = DocumentHeaderDeserializer.class)
	@JsonSerialize		(keyUsing = DocumentHeaderSerializer.class)
	@XmlAnyAttribute
	private Map<QName, String> header = new HashMap<>();

	@XmlElement(name="title", namespace=Document.NS_WEBLYZARD)
	private String title;
	
	@XmlElement(name="body")
	private String body;
	
	/**
	 * attributes required for the annotation handling
	 */
	@JsonProperty("body_annotation")
	@XmlElement(name="body_annotation", namespace=Document.NS_WEBLYZARD)
	private List<Annotation> bodyAnnotation;
	
	@JsonProperty("title_annotation")
	@XmlElement(name="title_annotation", namespace=Document.NS_WEBLYZARD)
	private List<Annotation> titleAnnotations;
	
	/**
	 *  Elements used in the output (and input)
	 **/ 
	@JsonProperty("sentences")
	@XmlElement(name="sentence", namespace=Document.NS_WEBLYZARD)
	private List<Sentence> sentences;
	
	@XmlAttribute(name="id", namespace=Document.NS_WEBLYZARD) 
	private String id;
	
	@XmlAttribute(name="format", namespace=Document.NS_DUBLIN_CORE)
	private String format;
	
	@JsonProperty("lang")
	@XmlAttribute(name="xml:lang")
	private String lang;
	
	@XmlAttribute(namespace=Document.NS_WEBLYZARD)
	private String nilsimsa;
	
	// private field that contains all annotations after the
	// documents finalization
	@XmlElement(name="annotation", namespace=Document.NS_WEBLYZARD)
	private List<Annotation> annotations;


	// empty constructor required by JAXB
	public Document() {}
	
	public Document(String body) {
		this.title = ""; 
		this.body = body;
	}
	
	public Document(String title, String content, Map<QName, String> header) {
		this.title = title;
		this.body = content;
		this.header = header;
	}
	
	/** getter / setter **/

	public Map<QName, String> getHeader() {
		return header;
	}

	public Document setHeader(Map<QName, String> header) {
		this.header = header;
		return this;
	}

	public String getTitle() {
		return title;
	}

	public Document setTitle(String title) {
		this.title = title;
		return this;
	}

	public String getBody() {
		return body;
	}

	public Document setBody(String body) {
		this.body = body;
		return this;
	}

	public List<Annotation> getBodyAnnotations() {
		return bodyAnnotation != null ? bodyAnnotation : Collections.<Annotation>emptyList(); 
	}

	public Document setBodyAnnotations(List<Annotation> bodyAnnotations) {
		this.bodyAnnotation = bodyAnnotations;
		return this;
	}

	public List<Annotation> getTitleAnnotations() {
		return titleAnnotations != null ? titleAnnotations : Collections.<Annotation>emptyList();
	}

	public Document setTitleAnnotations(List<Annotation> titleAnnotations) {
		this.titleAnnotations = titleAnnotations;
		return this;
	}

	public List<Sentence> getSentences() {
		return sentences;
	}

	public Document setSentences(List<Sentence> sentences) {
		this.sentences = sentences;
		return this;
	}

	public String getId() {
		return id;
	}

	public Document setId(String id) {
		this.id = id;
		return this;
	}

	public String getFormat() {
		return format;
	}

	public Document setFormat(String format) {
		this.format = format;
		return this;
	}

	public String getLang() {
		return lang;
	}

	public Document setLang(String lang) {
		this.lang = lang;
		return this;
	}

	public String getNilsimsa() {
		return nilsimsa;
	}

	public Document setNilsimsa(String nilsimsa) {
		this.nilsimsa = nilsimsa;
		return this;
	}

	public List<Annotation> getAnnotations() {
		return annotations;
	}

	public Document setAnnotations(List<Annotation> annotations) {
		this.annotations = annotations;
		return this;
	}

	/**
	 * @param document
	 * @return the XML representation of the given document
	 */
    public static String getXmlRepresentation(Document document) throws JAXBException {
    	StringWriter stringWriter = new StringWriter();
    	JAXBElement<Document> jaxbElement = new JAXBElement<Document>(
    			new QName(Document.NS_WEBLYZARD, "wl:page", "wl"), Document.class, document);
    	JAXBContext jaxbContext = JAXBContext.newInstance(Document.class);
    	Marshaller xmlMarshaller = jaxbContext.createMarshaller();
    	xmlMarshaller.setProperty(Marshaller.JAXB_FORMATTED_OUTPUT, true);
    	xmlMarshaller.marshal(jaxbElement, stringWriter);
    	return stringWriter.toString();
    }
    
    /**
     * 
     * @param xmlString
     * @return
     */
    public static Document unmarshallDocumentXmlString(String xmlString) throws JAXBException {
    	JAXBContext jaxbContext = JAXBContext.newInstance(Document.class);
    	Unmarshaller unmarshaller = jaxbContext.createUnmarshaller();
    	StringReader reader = new StringReader(xmlString);
    	return (Document) unmarshaller.unmarshal(reader);
    }
    
}
