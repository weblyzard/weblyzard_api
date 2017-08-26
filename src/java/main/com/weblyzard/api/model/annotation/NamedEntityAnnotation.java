package com.weblyzard.api.model.annotation;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.databind.annotation.JsonSerialize;
import com.weblyzard.api.datatype.MD5Digest;
import com.weblyzard.api.model.document.Document;
import com.weblyzard.api.serialize.json.CompactAnnotationSerializer;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.XmlElement;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.experimental.Accessors;

/**
 * A compact annotation. This is similar to the standard annotation but with extra properties rather
 * than the nested gate features.
 *
 * @author Max Goebel <goebel@weblyzard.com>
 */
@Data
@EqualsAndHashCode(callSuper = true)
@Accessors(chain = true)
@XmlAccessorType(XmlAccessType.FIELD)
@JsonSerialize(using = CompactAnnotationSerializer.class)
@JsonIgnoreProperties({
    "sentence",
    "start",
    "end",
    "surfaceForm",
    "scoreName",
    "grounded",
    "pos",
    "md5sum",
    "@type"
})
public class NamedEntityAnnotation extends CompactAnnotation {

    /** */
    private static final long serialVersionUID = 1L;

    //	@XmlElement(name="entities", namespace=Document.NS_WEBLYZARD)
    //	private List<AnnotationSurface> entities;

    @XmlAttribute(name = "entityType", namespace = Document.NS_WEBLYZARD)
    private String entityType;

    @XmlAttribute(name = "profileName", namespace = Document.NS_WEBLYZARD)
    private String profileName;

    private double confidence;

    private double score;
    private String scoreName;
    private boolean grounded = true;

    @XmlElement(name = "properties", namespace = Document.NS_WEBLYZARD)
    private Map<String, String> properties;

    //Required by JAX-B
    public NamedEntityAnnotation() {
        super();
    }

    /**
     * Creates a new Annotation with one AnnotationFeature.
     *
     * @param start offset where the token starts
     * @param end offset where the token ends
     * @param sentenceId sentence Id
     * @param confidence of the entity matching this token
     * @param preferredName
     *     <p>identifier of the entity matching this token
     * @param profile where the entity was retrieved from
     * @param entityType
     * @param score custom score point to be computed by NER system
     */
    public NamedEntityAnnotation(
            int start,
            int end,
            int sentence,
            MD5Digest md5sum,
            String key,
            String surfaceForm,
            String preferredName,
            String profileName,
            String entityType,
            double confidence,
            double score,
            String scoreName) {
        super(key, surfaceForm, preferredName, start, end, sentence, md5sum, entityType);
        this.profileName = profileName;
        this.entityType = entityType;
        this.confidence = confidence;
        this.score = score;
        this.scoreName = scoreName;
        this.setEntities(new ArrayList<>());
        this.properties = new HashMap<>();
        if (end > start)
            addSurface(new AnnotationSurface(start, end, sentence, md5sum, surfaceForm));
    }

    @JsonIgnore
    public String getTopEntityId() {
        return getPreferredName();
    }

    /** @param annotation */
    public NamedEntityAnnotation(final NamedEntityAnnotation annotation) {
        this(
                annotation.getStart(),
                annotation.getEnd(),
                annotation.getSentence(),
                annotation.getMd5sum(),
                annotation.getKey(),
                annotation.getSurfaceForm(),
                annotation.getPreferredName(),
                annotation.getProfileName(),
                annotation.getEntityType(),
                annotation.confidence,
                annotation.score,
                annotation.scoreName);
    }

    /**
     * Returns true if both Annotations share at least one character at the start or end.
     *
     * @param a
     * @return
     */
    public boolean overlaps(NamedEntityAnnotation a) {
        return (a.getMd5sum() == getMd5sum())
                && ((getStart() >= a.getStart() && getStart() < a.getEnd())
                        || (a.getStart() >= getStart() && a.getEnd() < getEnd()));
    }

    @JsonIgnore
    public int getLength() {
        return this.getEnd() - this.getStart();
    }
}
