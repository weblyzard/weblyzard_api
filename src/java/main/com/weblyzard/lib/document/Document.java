package com.weblyzard.lib.document;

import java.io.Serializable;
import java.io.StringReader;
import java.io.StringWriter;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.logging.Logger;

import javax.xml.bind.JAXBContext;
import javax.xml.bind.JAXBElement;
import javax.xml.bind.JAXBException;
import javax.xml.bind.Marshaller;
import javax.xml.bind.Unmarshaller;
import javax.xml.bind.annotation.XmlAnyAttribute;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.namespace.QName;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import com.fasterxml.jackson.databind.annotation.JsonSerialize;
import com.google.common.base.Joiner;
import com.weblyzard.lib.document.annotation.Annotation;
import com.weblyzard.lib.document.serialize.json.DocumentHeaderDeserializer;
import com.weblyzard.lib.document.serialize.json.DocumentHeaderSerializer;
import com.weblyzard.lib.string.nilsimsa.Nilsimsa;

@XmlRootElement(name="page", namespace=Document.NS_WEBLYZARD)
@JsonIgnoreProperties(ignoreUnknown = true)
public class Document implements Serializable {
	
	private final static long serialVersionUID = 1L;
	public final static String NS_WEBLYZARD = "http://www.weblyzard.com/wl/2013#";
	public final static String NS_DUBLIN_CORE = "http://purl.org/dc/elements/1.1/";
	
	public final static Joiner SENTENCE_JOINER = Joiner.on("\n");
	
	private static Logger logger = Logger.getLogger(Document.class.getName());
	
	public final static QName WL_KEYWORD_ATTR = new QName(NS_DUBLIN_CORE, "subject");
	
	@JsonDeserialize	(keyUsing = DocumentHeaderDeserializer.class)
	@JsonSerialize		(keyUsing = DocumentHeaderSerializer.class)
	@XmlAnyAttribute
	private Map<QName, String> header = new HashMap<>();

	@XmlElement(name="title", namespace=Document.NS_WEBLYZARD)
	private String title;
	
	@XmlElement(name="body")
	private String body;
	
	// attributes required for the annotation handling
	@XmlElement(name="body_annotation", namespace=Document.NS_WEBLYZARD)
	private List<Annotation> body_annotation;
	
	@XmlElement(name="title_annotation", namespace=Document.NS_WEBLYZARD)
	private List<Annotation> title_annotation;
	
	//
	// Elements used in the output (and input)
	// 
	@XmlElement(name="sentence", namespace=Document.NS_WEBLYZARD)
	private List<Sentence> sentence;
	
	@XmlAttribute(name="id", namespace=Document.NS_WEBLYZARD) 
	private String id;
	
	@XmlAttribute(name="format", namespace=Document.NS_DUBLIN_CORE)
	private String format;
	
	@XmlAttribute(name="xml:lang")
	private String lang;
	
	@XmlAttribute(namespace=Document.NS_WEBLYZARD)
	private String nilsimsa;
	
	// private field that contains all annotations after the
	// documents finalization
	@XmlElement(name="annotation", namespace=Document.NS_WEBLYZARD)
	private List<Annotation> annotation;


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

	public List<Annotation> getBody_annotation() {
		return body_annotation != null ? body_annotation : Collections.<Annotation>emptyList(); 
	}

	public Document setBody_annotation(List<Annotation> body_annotation) {
		this.body_annotation = body_annotation;
		return this;
	}

	public List<Annotation> getTitle_annotation() {
		return title_annotation != null ? title_annotation : Collections.<Annotation>emptyList();
	}

	public Document setTitle_annotation(List<Annotation> title_annotation) {
		this.title_annotation = title_annotation;
		return this;
	}

	public List<Sentence> getSentence() {
		return sentence;
	}

	public Document setSentence(List<Sentence> sentence) {
		this.sentence = sentence;
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

	public List<Annotation> getAnnotation() {
		return annotation;
	}

	public Document setAnnotation(List<Annotation> annotation) {
		this.annotation = annotation;
		return this;
	}

	/**
	 * Clears the content and annotation fields. 
	 * This step is required to 
	 *   a) prevent content from being included twice in the final result.
	 *   b) set the annotation field
	 */
	public void finalizeDocument() {
		// clear content fields
		title = null;
		body = null;
		
		// process and clear annotation fields
		annotation = new ArrayList<>(getTitle_annotation().size() + getBody_annotation().size());
		annotation.addAll(getTitle_annotation());
		annotation.addAll(getBody_annotation());
		
		title_annotation = null;
		body_annotation = null;
	}
	
	/**
	 * computes the Nilsimsa hash of the document (title + content)
	 */
	public void computeNilsimsaHash() {
		Nilsimsa n = new Nilsimsa();
		if (sentence != null) {
			// do not add the title to the nilsimsa hash computation, since
			// twitter blogs use a standardized (!) title.
			sentence.stream()
				.forEach(s -> n.update(s.getText()));
		}
		nilsimsa = n.hexdigest();
	}		

	
	/**
	 * @param document
	 * @return the XML representation of the given document
	 */
    public static String getXmlRepresentation(Document document) {
        StringWriter s = new StringWriter();
        JAXBElement<Document> jaxbElement = new JAXBElement<Document>(
                new QName(Document.NS_WEBLYZARD, "wl:page", "wl"), Document.class, document);
        try {
        	JAXBContext jaxbContext = JAXBContext.newInstance(Document.class);
            Marshaller xmlMarshaller = jaxbContext.createMarshaller();
            xmlMarshaller.setProperty(Marshaller.JAXB_FORMATTED_OUTPUT, true);
            xmlMarshaller.marshal(jaxbElement, s);
        } catch (JAXBException e) { // TODO: move the exception to the method's consumers
            logger.severe("Creation of the XML document for content_id "
                    + document.id +" failed due to a JAXB exception.");
            e.printStackTrace();
        }
        return s.toString();
    }
    
	public static Document unmarshallDocumentXMLString(String xml) {
		try {
			JAXBContext jaxbContext = JAXBContext.newInstance(Document.class);
			Unmarshaller unmarshaller = jaxbContext.createUnmarshaller();
			StringReader reader = new StringReader(xml);
			return (Document) unmarshaller.unmarshal(reader);
		} catch (JAXBException e) {
			e.printStackTrace();
		}
		return null;
	}
}
