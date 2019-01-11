package com.weblyzard.api.model.flow;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.experimental.Accessors;

@Data
@Accessors(chain = true)
@NoArgsConstructor
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
