package com.weblyzard.api.client;

import java.io.IOException;
import java.net.Socket;
import java.net.UnknownHostException;
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
		
		String host = basicClient.getBaseTarget().getUri().getHost();
		int port = basicClient.getBaseTarget().getUri().getPort();
		
		try {
			s = new Socket(host, port);
			return true;
		} catch (IOException e) {
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
