package com.weblyzard.lib.document.serialize.xml;

import javax.xml.bind.annotation.adapters.XmlAdapter;

/**
 * Enables empty attributes for boolean values that are false
 * @author http://stackoverflow.com/questions/6552740/jaxb-suppress-boolean-attribute-if-false
 *
 */
public class BooleanAdapter extends XmlAdapter<Boolean, Boolean> {

    @Override
    public Boolean unmarshal(Boolean v) throws Exception {
        return Boolean.TRUE.equals(v);
    }

    @Override
    public Boolean marshal(Boolean v) throws Exception {
        if(v) {
            return v;
        }
        return null;
    }

}