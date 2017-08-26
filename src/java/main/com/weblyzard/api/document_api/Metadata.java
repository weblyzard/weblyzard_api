package com.weblyzard.api.document_api;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class Metadata {

    public String author;

    @JsonProperty("published_date")
    public String publishedDate;
}
