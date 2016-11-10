package com.weblyzard.api.client;

import java.net.Socket;
import java.util.logging.Logger;

public class TestClientBase {
	
	protected Logger logger = Logger.getLogger(getClass().getName());
	
	/**
	 * checks if a network service is running 
	 * 
	 * @param host host the server is running on
	 * @param port port the server is listening on 
	 * @return
	 */
	public boolean weblyzardServiceAvailable(BasicClient basicClient) {
		
		
		Socket s = null;
		
		String host = basicClient.getTarget().getUri().getHost();
		int port = basicClient.getTarget().getUri().getPort();
		
		try {
			s = new Socket(host, port);
			return true;
		} catch (Exception e) {
			logger.info("service is not available :"+host+":"+port);
			return false;
		} finally {
			if (s != null)
				try {
					s.close();
				} catch (Exception e) {
				}
		}
	}
}
