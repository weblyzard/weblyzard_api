package com.weblyzard.api.model.recognyze;

import java.util.Set;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.experimental.Accessors;

@Data
@Accessors(chain = true)
@NoArgsConstructor
public class RecognyzeResult {

    private String key;
    private Set<SurfaceForm> surfaceForms;
    private String entityType;
    private double confidence;
}
