package com.weblyzard.api.model.document;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.weblyzard.api.model.annotation.Annotation;
import java.util.List;
import javax.xml.bind.JAXBException;
import javax.xml.bind.annotation.XmlAttribute;
import lombok.Data;
import lombok.experimental.Accessors;

/**
 * Data format used to return to the Web service client
 *
 * @author albert@weblyzard.com
 */
@Data
@Accessors(chain = true)
public class XmlDocument {

    @JsonProperty("content_id")
    @XmlAttribute(name = "content_id", required = true)
    private String contentId;

    @JsonProperty("xml_content")
    @XmlAttribute(name = "xml_content", required = true)
    private String xmlContent;

    private String nilsimsa;
    private List<Annotation> annotation;
    private String error;

    public XmlDocument(Document document, List<Annotation> annotation) throws JAXBException {
        contentId = document.getId();
        nilsimsa = document.getNilsimsa();
        this.annotation = annotation;
        xmlContent = Document.getXmlRepresentation(document);
    }
}
