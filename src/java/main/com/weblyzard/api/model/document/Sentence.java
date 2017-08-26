package com.weblyzard.api.model.document;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.weblyzard.api.datatype.MD5Digest;
import com.weblyzard.api.serialize.xml.BooleanAdapter;
import java.io.Serializable;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.XmlValue;
import javax.xml.bind.annotation.adapters.XmlJavaTypeAdapter;
import lombok.Data;
import lombok.experimental.Accessors;
import org.eclipse.persistence.oxm.annotations.XmlCDATA;

/**
 * webLyzard Sentence class
 *
 * @author weichselbraun@weblyzard.com
 */
@Data
@Accessors(chain = true)
@XmlAccessorType(XmlAccessType.FIELD)
public class Sentence implements Serializable {
    private static final long serialVersionUID = 1L;

    private static final String HTML_ENTITY_QUOT = "&quot;";

    @JsonProperty("md5sum")
    @XmlAttribute(name = "id", namespace = Document.NS_WEBLYZARD)
    @XmlJavaTypeAdapter(MD5Digest.class)
    private MD5Digest id;

    /** The POS dependency tree of the given sentence. */
    @XmlAttribute(name = "pos", namespace = Document.NS_WEBLYZARD)
    private String pos;

    @XmlAttribute(name = "dependency", namespace = Document.NS_WEBLYZARD)
    private String dependency;

    @XmlAttribute(name = "token", namespace = Document.NS_WEBLYZARD)
    private String token;

    @JsonProperty("is_title")
    @XmlAttribute(name = "is_title", namespace = Document.NS_WEBLYZARD)
    @XmlJavaTypeAdapter(BooleanAdapter.class)
    private Boolean isTitle;

    @JsonProperty("text")
    @XmlValue
    @XmlCDATA
    private String text;

    @JsonProperty("sem_orient")
    @XmlAttribute(name = "sem_orient", namespace = Document.NS_WEBLYZARD)
    private double semOrient;

    @XmlAttribute(name = "significance", namespace = Document.NS_WEBLYZARD)
    private double significance;

    public Sentence(String text) {
        this.text = text;
        id = MD5Digest.fromText(text);
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

    public String getText() {
        return text.replace(HTML_ENTITY_QUOT, "\"");
    }

    public Sentence setText(String text) {
        // required to allow marshalling of the XML document (!)
        this.text = text.replace("\"", HTML_ENTITY_QUOT);
        return this;
    }

    public Sentence setPos(String pos) {
        // required for handling double quotes in POS tags.
        this.pos = pos.replace("\"", HTML_ENTITY_QUOT);
        return this;
    }

    public String getPos() {
        return pos != null ? pos.replace(HTML_ENTITY_QUOT, "\"") : pos;
    }

    public Boolean isTitle() {
        return Boolean.TRUE.equals(isTitle);
    }
}
