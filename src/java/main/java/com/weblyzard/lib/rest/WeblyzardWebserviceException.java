package com.weblyzard.lib.rest;


import javax.ws.rs.WebApplicationException;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;



public class WeblyzardWebserviceException extends WebApplicationException {
	
	/** */
	private static final long serialVersionUID = -6538332318545568381L;

	public WeblyzardWebserviceException(String message) {
		super(Response.status(Response.Status.BAD_REQUEST)
				.entity(message).type(MediaType.TEXT_PLAIN).build());
	}
}