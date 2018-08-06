package com.weblyzard.api.model.annotation;

import java.io.Serializable;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.adapters.XmlJavaTypeAdapter;
import com.fasterxml.jackson.annotation.JsonTypeInfo;
import com.fasterxml.jackson.annotation.JsonTypeInfo.Id;
import com.weblyzard.api.datatype.MD5Digest;
import com.weblyzard.api.model.Span;
import com.weblyzard.api.model.document.LegacyDocument;
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
@JsonTypeInfo(use = Id.NONE)
public class Annotation extends EntityDescriptor implements Serializable, Span {

    @XmlAttribute(name = "surfaceForm", namespace = LegacyDocument.NS_WEBLYZARD)
    private String surfaceForm;

    @XmlAttribute(name = "start", namespace = LegacyDocument.NS_WEBLYZARD)
    private int start;

    @XmlAttribute(name = "end", namespace = LegacyDocument.NS_WEBLYZARD)
    private int end;

    @XmlAttribute(name = "pos", namespace = LegacyDocument.NS_WEBLYZARD)
    private String pos;

    @XmlAttribute(name = "sentence", namespace = LegacyDocument.NS_WEBLYZARD)
    private int sentence;

    @XmlAttribute(name = "md5sum", namespace = LegacyDocument.NS_WEBLYZARD)
    @XmlJavaTypeAdapter(MD5Digest.class)
    private MD5Digest md5sum;

    @XmlAttribute(name = "confidence", namespace = LegacyDocument.NS_WEBLYZARD)
    private double confidence;

    public Annotation(String key) {
        super(key);
    }

    public static Annotation build(String key) {
        return new Annotation(key);
    }

}
