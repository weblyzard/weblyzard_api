package com.weblyzard.api.model.document_api;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.experimental.Accessors;

@Data
@Accessors(chain = true)
@AllArgsConstructor
public class Metadata {

    private String author;

    @JsonProperty("published_date")
    private String publishedDate;
}
