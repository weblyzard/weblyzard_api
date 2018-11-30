package com.weblyzard.api.model.annotation;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.xml.bind.annotation.XmlAttribute;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.weblyzard.api.model.document.LegacyDocument;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.NonNull;
import lombok.RequiredArgsConstructor;
import lombok.experimental.Accessors;

/**
 * A descriptor for an entity such as a person, organization, location or event.
 * 
 * @author Albert Weichselbraun
 *
 */
@Data
@Accessors(chain = true)
@NoArgsConstructor
@RequiredArgsConstructor()
public class EntityDescriptor {

    /** Unique identifier (such as a DBpedia resource URL) of the entity. */
    @NonNull
    @XmlAttribute(name = "key", namespace = LegacyDocument.NS_WEBLYZARD)
    private String key;

    @JsonProperty("preferred_name")
    @XmlAttribute(name = "preferred_name", namespace = LegacyDocument.NS_WEBLYZARD)
    private String preferredName;

    /** This field determines the entity's type (e.g. Person, Organiatzion, etc.). */
    @JsonProperty("entity_type")
    @XmlAttribute(name = "entity_type", namespace = LegacyDocument.NS_WEBLYZARD, required = false)
    private String entityType;

    /** This field allows adding custom annotations to entities. */
    @JsonProperty("entity_metadata")
    @XmlAttribute(name = "entity_metadata", namespace = LegacyDocument.NS_WEBLYZARD)
    private Map<String, List<String>> entityMetadata = new HashMap<>();

    public Annotation annotation() {
        return (Annotation) this;
    }

    public CompactAnnotation compactAnnotation() {
        return (CompactAnnotation) this;
    }
}
