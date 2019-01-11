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
    /** Whether to compress the communication between server and client. */
    private boolean useCompression = false;

    /** The service prefix such as '/jeremia' or ':63001'. */
    private String servicePrefix;

    private boolean debug = System.getenv("WEBLYZARD_API_DEBUG") != null;

    /**
     * Sets the service prefix to the defaultServicePrefix provided by the calling class, if no
     * custom prefix has been specified.
     * 
     * @param defaultServicePrefix the prefix to use if no custom prefix has been set
     */
    public String getServicePrefix(String defaultServicePrefix) {
        return servicePrefix == null ? defaultServicePrefix : servicePrefix;
    }
}
