package com.weblyzard.api.model.johndoe;

import java.util.List;
import java.util.Map;

/**
 * The {@link JohnDoeDocument} class is used to represent JohnDoeDocuments.
 * 
 * @author sandro.hoerler@htwchur.ch
 *
 */
public class JohnDoeDocument {
    private String profileName;
    private String baseUrl;
    private List<String> names;
    private Map<String, String> nameAnnonIdMap;

    /**
     * 
     * Default constructor for {@link JohnDoeDocument} {@link profileName}} {@link baseUrl} and
     * {@link names} must be set to get document processed by johndoe.
     * 
     * @param profileName Profile name
     * @param baseUrl Url of document
     * @param names extracted names for annonymization
     */
    public JohnDoeDocument(String profileName, String baseUrl, List<String> names) {
        this.profileName = profileName;
        this.baseUrl = baseUrl;
        this.names = names;
    }

    public JohnDoeDocument() {}

    public String getProfileName() {
        return profileName;
    }

    public void setProfileName(String profileName) {
        this.profileName = profileName;
    }

    public String getBaseUrl() {
        return baseUrl;
    }

    public void setBaseUrl(String baseUrl) {
        this.baseUrl = baseUrl;
    }

    public List<String> getNames() {
        return names;
    }

    public void setNames(List<String> names) {
        this.names = names;
    }

    public Map<String, String> getNameAnnonIdMap() {
        return nameAnnonIdMap;
    }

    public void setNameAnnonIdMap(Map<String, String> nameAnnonIdMap) {
        this.nameAnnonIdMap = nameAnnonIdMap;
    }

}
