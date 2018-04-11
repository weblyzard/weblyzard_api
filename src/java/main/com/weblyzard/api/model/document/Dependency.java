package com.weblyzard.api.model.document;

import lombok.Value;

/**
 * A dependency with the index of the dependency's parent ("-1" indicates the root element) and the
 * corresponding label.
 * 
 * @author Albert Weichselbraun
 */
@Value
public class Dependency {
    private final int parent;
    private final String label;
}
