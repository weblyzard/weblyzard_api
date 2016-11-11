package com.weblyzard.api.joseph;

import java.io.Serializable;

/**
 * Simple Wrapper Class containing one feature and the calculated significance
 * of this.
 * 
 * @author philipp.kuntschik@htwchur.ch
 * 
 */
public class Significance implements Serializable {

	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;

	/**
	 * The feature
	 */
	public String feature;

	/**
	 * significance of the feature
	 */
	public float significance;



	/**
	 * simple constructor
	 * 
	 * @param feature
	 *            The analyzed feature
	 * @param significance
	 *            The calculated significance
	 */
	public Significance(String feature, float significance) {
		this.feature = feature;
		this.significance = significance;
	}

}
