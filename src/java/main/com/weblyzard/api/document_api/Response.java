package com.weblyzard.api.document_api;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

@Data
public class Response {

    @JsonProperty("_id")
    public String id;

    public boolean created;
}
