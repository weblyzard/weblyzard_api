/**
 * The {@link com.weblyzard.api.model.document.Document} and {@link
 * com.weblyzard.api.model.document.Sentence} classes used to encapsulate the webLyzardXML format.
 */
@XmlSchema(
    elementFormDefault = XmlNsForm.QUALIFIED,
    namespace = Document.NS_WEBLYZARD,
    xmlns = {
        @XmlNs(prefix = "wl", namespaceURI = Document.NS_WEBLYZARD),
        @XmlNs(prefix = "dc", namespaceURI = Document.NS_DUBLIN_CORE)
    }
)
package com.weblyzard.api.model.document;

import javax.xml.bind.annotation.XmlNs;
import javax.xml.bind.annotation.XmlNsForm;
import javax.xml.bind.annotation.XmlSchema;
