package com.weblyzard.api.model.document_api;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.experimental.Accessors;

@Data
@Accessors(chain = true)
@NoArgsConstructor
public class Response {

    @JsonProperty("_id")
    private String id;

    private boolean created;
}
