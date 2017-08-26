package com.weblyzard.api.model.jairo;

import java.io.Serializable;
import java.util.HashMap;
import java.util.Map;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import lombok.experimental.Accessors;

/** @author Norman Suesstrunk */
@Data
@Accessors(chain = true)
@EqualsAndHashCode
@NoArgsConstructor
public class Profile implements Serializable {

    private static final long serialVersionUID = 1L;

    private Map<String, String> types = new HashMap<>();
    private String sparqlEndpoint;
    private String query;

    public void addType(String key, String value) {
        types.put(key, value);
    }
}
