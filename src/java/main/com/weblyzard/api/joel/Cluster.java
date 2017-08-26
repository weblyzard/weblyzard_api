package com.weblyzard.api.joel;

import java.util.List;
import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class Cluster {

    private List<KeywordDocument> docs;
    private String label;
}
