package com.weblyzard.api.model.joel;

import java.util.List;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.experimental.Accessors;

@Data
@Accessors(chain = true)
@AllArgsConstructor
public class Cluster {

    private List<KeywordDocument> docs;
    private String label;
}
