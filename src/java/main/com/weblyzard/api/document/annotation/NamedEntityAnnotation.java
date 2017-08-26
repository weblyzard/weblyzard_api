package com.weblyzard.api.document.annotation;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.databind.annotation.JsonSerialize;
import com.weblyzard.api.datatype.MD5Digest;
import com.weblyzard.api.document.serialize.json.CompactAnnotationSerializer;
import com.weblyzard.api.model.document.Document;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.XmlElement;

/**
 * A compact annotation. This is similar to the standard annotation but with extra properties rather
 * than the nested gate features.
 *
 * @author Max Goebel <goebel@weblyzard.com>
 */
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
        this.entities = new ArrayList<>();
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
        if (a.getMd5sum() == getMd5sum()) {
            if ((getStart() >= a.getStart() && getStart() < a.getEnd())
                    || (a.getStart() >= getStart() && a.getEnd() < getEnd())) {
                return true;
            }
        }
        return false;
    }

    @JsonIgnore
    public int getLength() {
        return this.getEnd() - this.getStart();
    }

    public Map<String, String> getProperties() {
        return properties;
    }

    public void setProperties(Map<String, String> properties) {
        this.properties = properties;
    }

    //	public List<AnnotationSurface> getEntities() {
    //		return entities;
    //	}
    //
    //	public void setEntities(List<AnnotationSurface> entities) {
    //		this.entities = entities;
    //	}

    public String getEntityType() {
        return entityType;
    }

    public void setEntityType(String entityType) {
        this.entityType = entityType;
    }

    public String getProfileName() {
        return profileName;
    }

    public void setProfileName(String profileName) {
        this.profileName = profileName;
    }

    public double getConfidence() {
        return confidence;
    }

    public void setConfidence(double confidence) {
        this.confidence = confidence;
    }

    public double getScore() {
        return score;
    }

    public void setScore(double score) {
        this.score = score;
    }

    public String getScoreName() {
        return scoreName;
    }

    public void setScoreName(String scoreName) {
        this.scoreName = scoreName;
    }

    public boolean isGrounded() {
        return grounded;
    }

    public void setGrounded(boolean grounded) {
        this.grounded = grounded;
    }
}
