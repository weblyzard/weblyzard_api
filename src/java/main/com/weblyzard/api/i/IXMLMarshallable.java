package com.weblyzard.api.i;

import java.io.InputStream;

import javax.xml.bind.JAXBException;

public interface IXMLMarshallable<C> {

	public String marshal() throws JAXBException;



	public C unmarshal(String s) throws JAXBException;



	public C unmarshal(InputStream inputStream) throws JAXBException;
}
