package com.weblyzard.api.model.joel;

import java.io.Serializable;
import java.util.List;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.experimental.Accessors;

@Data
@Accessors(chain = true)
@AllArgsConstructor
public class Cluster implements Serializable {

    private static final long serialVersionUID = 1L;

    private List<KeywordDocument> docs;
    private String label;
}
