package com.weblyzard.api.document_api;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

@Data
public class Request {

    @JsonProperty("repository_id")
    private String repositoryId;

    private String title;
    private String uri;
    private String content;

    @JsonProperty("content_type")
    private String contentType;

    @JsonProperty("meta_data")
    private Metadata metadata;
}
