package com.weblyzard.api.joseph;

import java.io.Serializable;

import javax.xml.bind.annotation.XmlRootElement;

/**
 * Domain Transfer Object defining the interface for other services to use this
 * Webservice. DaoLearnResponse is returned by the service after a
 * <code>webservice.learn()</code> or a <code>webservice.retrain()</code> call.
 * 
 * @author Philipp Kuntschik
 * 
 */
@XmlRootElement
public class LearnResponse implements Serializable {

	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	public int statuscode;
	public String message;



	public LearnResponse() {
	}



	public LearnResponse setMessage(String message) {
		this.message = message;
		return this;
	}



	public LearnResponse setStatuscode(int statuscode) {
		this.statuscode = statuscode;
		return this;
	}

}
