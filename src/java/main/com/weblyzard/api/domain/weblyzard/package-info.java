/**
 * The {@link com.weblyzard.Document.document.Document} and {@link com.weblyzard.lib.document.Sentence} 
 * classes used for the webLyzardXML format.
 */

@XmlSchema(
	    elementFormDefault=XmlNsForm.QUALIFIED,
	    namespace=Document.NAMESPACE_WEBLYZARD,
	    xmlns={@XmlNs(prefix="wl", namespaceURI=Document.NAMESPACE_WEBLYZARD),
	           @XmlNs(prefix="dc", namespaceURI=Document.NAMESPACE_DUBLIN_CORE)}
	)
package com.weblyzard.api.domain.weblyzard;

import javax.xml.bind.annotation.XmlNs;
import javax.xml.bind.annotation.XmlNsForm;
import javax.xml.bind.annotation.XmlSchema;

