package com.weblyzard.api.client;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.experimental.Accessors;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Accessors(chain = true)
public class WebserviceClientConfig {

    private String url = System.getenv("WEBLYZARD_API_URL");
    private String username = System.getenv("WEBLYZARD_API_USER");
    private String password = System.getenv("WEBLYZARD_API_PASS");

    /** the service prefix such as `/jeremia` or `:63001` */
    private String servicePrefix;

    private boolean debug = System.getenv("WEBLYZARD_API_DEBUG") != null;

    /**
     * Sets the service prefix to the defaultServicePrefix provided by
     * the calling class, if no custom prefix has been specified. 
     */
    public void setServicePrefixIfEmpty(String defaultServicePrefix) {
        if (servicePrefix == null) {
            servicePrefix = defaultServicePrefix;
        }
    }
}
