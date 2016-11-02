package com.weblyzard.api.joseph;

import java.io.Serializable;

import javax.xml.bind.annotation.XmlRootElement;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

/**
 * 
 * @author philipp.kuntschik@htwchur.ch
 *
 */
@JsonIgnoreProperties(ignoreUnknown = true)
@XmlRootElement
public class Product implements Serializable {

	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	public String name;
	public int id;



	public Product(String name, int id) {
		this.name = name;
		this.id = id;
	}

}
