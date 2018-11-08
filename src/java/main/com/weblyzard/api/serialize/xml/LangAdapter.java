package com.weblyzard.api.serialize.xml;

import javax.xml.bind.annotation.adapters.XmlAdapter;
import com.weblyzard.api.model.Lang;

/**
 * Serialization and deserialization of {@link Lang} attributes.
 * 
 * @author Albert Weichselbraun
 */
public class LangAdapter extends XmlAdapter<String, Lang> {

    @Override
    public String marshal(Lang v) throws Exception {
        return v.toString();
    }

    @Override
    public Lang unmarshal(String v) throws Exception {
        return Lang.getLanguage(v).orElse(null);
    }

}
