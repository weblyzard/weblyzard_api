package com.weblyzard.api.model.jairo;

import java.io.Serializable;
import com.weblyzard.api.model.annotation.Annotation;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import lombok.experimental.Accessors;

/**
 * Describes the SPARQL endpoint and query used for metadata enrichment of {@link Annotation}s.
 * 
 * @author Norman Suesstrunk
 */
@Data
@Accessors(chain = true)
@EqualsAndHashCode
@NoArgsConstructor
public class Profile implements Serializable {

    private static final long serialVersionUID = 1L;

    private String sparqlEndpoint;
    private String query;

}
