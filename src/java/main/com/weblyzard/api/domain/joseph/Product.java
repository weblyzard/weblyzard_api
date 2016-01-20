package com.weblyzard.api.domain.joseph;

import javax.xml.bind.annotation.XmlRootElement;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

/**
 * 
 * @author philipp.kuntschik@htwchur.ch
 *
 */
@JsonIgnoreProperties(ignoreUnknown = true)
@XmlRootElement
public class Product {

	public String name;
	public int id;



	public Product(String name, int id) {
		this.name = name;
		this.id = id;
	}

}
