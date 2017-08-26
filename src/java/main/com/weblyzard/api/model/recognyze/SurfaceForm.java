package com.weblyzard.api.model.recognyze;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.experimental.Accessors;

@Data
@Accessors(chain = true)
@NoArgsConstructor
public class SurfaceForm {

    private String value;
    private int startIndex;
    private int endIndex;
    private boolean isContext;
    private double confidence;
}
