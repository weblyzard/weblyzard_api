package com.weblyzard.api.jairo;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.io.Serializable;
import java.util.HashMap;
import java.util.Map;
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.Setter;

/** @author Norman Suesstrunk */
@EqualsAndHashCode
public class Profile implements Serializable {

    private static final long serialVersionUID = 1L;

    private @Getter @Setter Map<String, String> types = new HashMap<>();

    @JsonProperty("sparqlEndpoint")
    private @Getter @Setter String sparqlEndpoint;

    @JsonProperty("query")
    private @Getter @Setter String query;

    public void addType(String key, String value) {
        types.put(key, value);
    }
}
