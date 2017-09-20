package com.weblyzard.api.model.document;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import com.fasterxml.jackson.databind.annotation.JsonSerialize;
import com.weblyzard.api.model.annotation.Annotation;
import com.weblyzard.api.serialize.json.DocumentHeaderDeserializer;
import com.weblyzard.api.serialize.json.DocumentHeaderSerializer;
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
import lombok.AccessLevel;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.experimental.Accessors;
/**
 * The {@link Document} and {@link Sentence} model classes used to represent documents.
 *
 * <p>The {@link Document} class also supports arbitrary meta data which is stored in the <code>
 * header</code> instance variable.
 *
 * <p>The static helper function {@link Document#getXmlRepresentation(Document)} and {@link
 * Document#unmarshallDocumentXmlString(String)} translate between {@link Document} objects and the
 * corresponding XML representations.
 *
 * @author weichselbraun@weblyzard.com
 */
@Data
@Accessors(chain = true)
@NoArgsConstructor
@XmlRootElement(name = "page", namespace = Document.NS_WEBLYZARD)
@JsonIgnoreProperties(ignoreUnknown = true)
@XmlAccessorType(XmlAccessType.FIELD)
public class Document implements Serializable {

    private static final long serialVersionUID = 1L;
    public static final String NS_WEBLYZARD = "http://www.weblyzard.com/wl/2013#";
    public static final String NS_DUBLIN_CORE = "http://purl.org/dc/elements/1.1/";

    /** The Attribute used to encode document keywords */
    public static final QName WL_KEYWORD_ATTR = new QName(NS_DUBLIN_CORE, "subject");

    @JsonDeserialize(keyUsing = DocumentHeaderDeserializer.class)
    @JsonSerialize(keyUsing = DocumentHeaderSerializer.class)
    @XmlAnyAttribute
    private Map<QName, String> header = new HashMap<>();

    @XmlElement(name = "title", namespace = Document.NS_WEBLYZARD)
    private String title;

    @XmlElement(name = "body")
    private String body;

    /** attributes required for the annotation handling */
    @JsonProperty("body_annotation")
    @XmlElement(name = "body_annotation", namespace = Document.NS_WEBLYZARD)
    private List<Annotation> bodyAnnotations;

    @JsonProperty("title_annotation")
    @XmlElement(name = "title_annotation", namespace = Document.NS_WEBLYZARD)
    private List<Annotation> titleAnnotations;

    /** Elements used in the output (and input) */
    @JsonProperty("sentences")
    @XmlElement(name = "sentence", namespace = Document.NS_WEBLYZARD)
    private List<Sentence> sentences;

    @XmlAttribute(name = "id", namespace = Document.NS_WEBLYZARD)
    private String id;

    @XmlAttribute(name = "format", namespace = Document.NS_DUBLIN_CORE)
    private String format;

    @JsonProperty("lang")
    @XmlAttribute(name = "lang", namespace = javax.xml.XMLConstants.XML_NS_URI)
    private String lang;

    @XmlAttribute(namespace = Document.NS_WEBLYZARD)
    private String nilsimsa;

    /**
     * This field contains all annotations after titleAnnotations and bodyAnnotations have been
     * merged. (i.e. after the document's finalization)
     */
    @Setter(AccessLevel.PROTECTED)
    @JsonProperty("annotations")
    @XmlElement(name = "annotation", namespace = Document.NS_WEBLYZARD)
    private List<Annotation> annotations;

    /** @param body the {@link Document}'s body */
    public Document(String body) {
        this.title = "";
        this.body = body;
    }

    /**
     * @param title the {@link Document}'s title
     * @param body the {@link Document}'s body
     * @param header a Map of optional meta data to store with the document
     */
    public Document(String title, String body, Map<QName, String> header) {
        this.title = title;
        this.body = body;
        this.header = header;
    }

    public Object clone() throws CloneNotSupportedException {
        return super.clone();
    }

    public List<Annotation> getBodyAnnotations() {
        return bodyAnnotations != null ? bodyAnnotations : Collections.<Annotation>emptyList();
    }

    public List<Annotation> getTitleAnnotations() {
        return titleAnnotations != null ? titleAnnotations : Collections.<Annotation>emptyList();
    }

    /**
     * Converts a {@link Document} to the corresponding webLyzard XML representation
     *
     * @param document The {@link Document} object to convert.
     * @return An XML representation of the given {@link Document} object.
     * @throws JAXBException
     */
    public static String getXmlRepresentation(Document document) throws JAXBException {
        StringWriter stringWriter = new StringWriter();
        JAXBElement<Document> jaxbElement =
                new JAXBElement<>(
                        new QName(Document.NS_WEBLYZARD, "page", "wl"), Document.class, document);
        JAXBContext jaxbContext = JAXBContext.newInstance(Document.class);
        Marshaller xmlMarshaller = jaxbContext.createMarshaller();
        xmlMarshaller.setProperty(Marshaller.JAXB_FORMATTED_OUTPUT, true);
        xmlMarshaller.marshal(jaxbElement, stringWriter);
        return stringWriter.toString();
    }

    /**
     * Converts a webLyzard XML Document to a {@link Document}.
     *
     * @param xmlString The webLyzard XML document to unmarshall
     * @return The {@link Document} instance corresponding to the xmlString
     * @throws JAXBException
     */
    public static Document unmarshallDocumentXmlString(String xmlString) throws JAXBException {
        JAXBContext jaxbContext = JAXBContext.newInstance(Document.class);
        Unmarshaller unmarshaller = jaxbContext.createUnmarshaller();
        StringReader reader = new StringReader(xmlString);
        return (Document) unmarshaller.unmarshal(reader);
    }
}
