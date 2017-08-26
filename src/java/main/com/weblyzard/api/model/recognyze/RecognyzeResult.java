package com.weblyzard.api.model.recognyze;

import java.util.Set;
import lombok.Data;
import lombok.experimental.Accessors;

@Data
@Accessors(chain = true)
public class RecognyzeResult {

    private String key;
    private Set<SurfaceForm> surfaceForms;
    private String entityType;
    private double confidence;
}
