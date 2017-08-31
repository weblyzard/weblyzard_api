package com.weblyzard.api.model.annotation;

import com.weblyzard.api.datatype.MD5Digest;
import com.weblyzard.api.model.document.Document;
import java.io.Serializable;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.adapters.XmlJavaTypeAdapter;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import lombok.ToString;
import lombok.experimental.Accessors;

/** @author norman.suesstrunk@htwchur.ch */
@Data
@Accessors(chain = true)
@NoArgsConstructor
@EqualsAndHashCode(callSuper = true)
@SuppressWarnings("serial")
@ToString(callSuper = true)
@XmlAccessorType(XmlAccessType.FIELD)
// @JsonSerialize(using = AnnotationSerializer.class)
public class Annotation extends EntityDescriptor implements Serializable {

    @XmlAttribute(name = "surfaceForm", namespace = Document.NS_WEBLYZARD)
    private String surfaceForm;

    @XmlAttribute(name = "start", namespace = Document.NS_WEBLYZARD)
    private int start;

    @XmlAttribute(name = "end", namespace = Document.NS_WEBLYZARD)
    private int end;

    @XmlAttribute(name = "pos", namespace = Document.NS_WEBLYZARD)
    private String pos;

    @XmlAttribute(name = "sentence", namespace = Document.NS_WEBLYZARD)
    private int sentence;

    @XmlAttribute(name = "md5sum", namespace = Document.NS_WEBLYZARD)
    @XmlJavaTypeAdapter(MD5Digest.class)
    private MD5Digest md5sum;

    @XmlAttribute(name = "confidence", namespace = Document.NS_WEBLYZARD)
    private double confidence;

    public Annotation(String key) {
        super(key);
    }

    public static Annotation build(String key) {
        return new Annotation(key);
    }
}
