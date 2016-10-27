package com.weblyzard.api.document_api;

public class Response {

	public boolean created;
	public String _id;



	public Response() {
	}



	public Response setCreated(boolean created) {
		this.created = created;
		return this;
	}



	public Response set_id(String _id) {
		this._id = _id;
		return this;
	}

}
