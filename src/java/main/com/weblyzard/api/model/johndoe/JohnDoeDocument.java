package com.weblyzard.api.model.johndoe;

import java.util.List;
import java.util.Map;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * The {@link JohnDoeDocument} class is used to represent JohnDoeDocuments.
 * 
 * @author sandro.hoerler@htwchur.ch
 *
 */
@Data
@NoArgsConstructor
public class JohnDoeDocument {
    private String profileName;
    private String baseUrl;
    private List<String> names;
    private Map<String, String> nameAnnonIdMap;

    /**
     * 
     * Default constructor for {@link JohnDoeDocument} {@link profileName}} {@link baseUrl} and {@link names} must be
     * set to get document processed by johndoe.
     * 
     * @param profileName Profile name
     * @param baseUrl Url of document
     * @param names for annonymization
     */
    public JohnDoeDocument(String profileName, String baseUrl, List<String> names) {
        this.profileName = profileName;
        this.baseUrl = baseUrl;
        this.names = names;
    }
}
