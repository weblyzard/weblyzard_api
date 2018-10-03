package com.weblyzard.api.client;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.experimental.Accessors;

@Data
@Accessors(chain = true)
@AllArgsConstructor
public class WebserviceClientConfig {

    private String url = System.getenv("WEBLYZARD_API_URL");
    private String username = System.getenv("WEBLYZARD_API_USER");
    private String password = System.getenv("WEBLYZARD_API_PASS");

    /** the service prefix such as `/jeremia` or `:63001` */
    private String servicePrefix;

    private boolean debug = System.getenv("WEBLYZARD_API_DEBUG") != null;

    /**
     * set the serivce prefix to the defaultServicePrefix if no custom one has been set.
     */
    public void setServicePrefixIfEmpty(String defaultServicePrefix) {
        if (servicePrefix == null) {
            servicePrefix = defaultServicePrefix;
        }
    }
}
