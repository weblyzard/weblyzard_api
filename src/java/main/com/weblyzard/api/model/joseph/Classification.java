package com.weblyzard.api.model.joseph;

import java.util.Map;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.experimental.Accessors;

@Data
@Accessors(chain = true)
@NoArgsConstructor
public class Classification {

    private String key;
    private Map<String, Double> terms;
    private double confidence;
    private String type;
}
