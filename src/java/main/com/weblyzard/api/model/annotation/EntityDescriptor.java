package com.weblyzard.api.model.annotation;

import com.weblyzard.api.model.document.Document;
import javax.xml.bind.annotation.XmlAttribute;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.NonNull;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class EntityDescriptor {

    /** unique identifier of the annotation */
    @NonNull
    @XmlAttribute(name = "key", namespace = Document.NS_WEBLYZARD)
    private String key;

    @XmlAttribute(name = "preferredName", namespace = Document.NS_WEBLYZARD)
    private String preferredName;

    @XmlAttribute(name = "annotationType", namespace = Document.NS_WEBLYZARD, required = false)
    private String annotationType;
}
