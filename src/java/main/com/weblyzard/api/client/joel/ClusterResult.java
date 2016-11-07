package com.weblyzard.api.client.joel;

import java.io.Serializable;


/**
 *  @author Norman Suesstrunk <norman.suesstrunk@htwchur.ch>
 *
 */
public class ClusterResult implements Serializable{
	
	private static final long serialVersionUID = 1L;

	private Topic topic; 
	
	private Cluster cluster;
	
	public ClusterResult() {}

	public ClusterResult(Topic topic, Cluster cluster) {
		this.topic = topic;
		this.cluster = cluster; 
	}

	public Topic getTopic() {
		return topic;
	}


	public void setTopic(Topic topic) {
		this.topic = topic;
	}
	
	public Cluster getCluster() {
		return this.cluster;
	}
}
