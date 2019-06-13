package com.weblyzard.api.model.document.partition;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * A dependency with the index of the dependency's parent ("-1" indicates the root element) and the corresponding label.
 * 
 * @author Albert Weichselbraun
 */
@Data
@AllArgsConstructor
@NoArgsConstructor
public class Dependency {

    private int parent;
    private String label;

}
