package com.weblyzard.api.model.document_api;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;
import lombok.experimental.Accessors;

@Data
@Accessors(chain = true)
public class Response {

    @JsonProperty("_id")
    private String id;

    private boolean created;
}
