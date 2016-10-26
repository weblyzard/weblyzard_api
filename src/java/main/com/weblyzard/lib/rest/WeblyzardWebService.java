package com.weblyzard.lib.rest;

import java.io.IOException;
import java.io.InputStream;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.jar.Attributes;
import java.util.jar.Manifest;
import java.util.logging.Level;
import java.util.logging.Logger;

import javax.servlet.ServletContext;
import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.core.Context;
import javax.ws.rs.core.MediaType;

import com.weblyzard.lib.logger.DictionaryLogHandler;


/**
 * Generic Weblyzard Web Service
 * 
 * @author Albert Weichselbraun <albert@weblyzard.com>
 * 
 * Provides logging and basic diagnostic functions
 * 
 * 
 */

public class WeblyzardWebService {
	
	@Context ServletContext context;

	private final static int DEFAULT_LOG_BUFFER = 50;
	private final static DictionaryLogHandler logDict = 
			new DictionaryLogHandler( DEFAULT_LOG_BUFFER);

	/**
	 * @return Returns a logger object for the given class
	 * 
	 *  Logging conventions:
	 *  ====================
	 *   a) severe  - critical messages
	 *   b) warning - non critical but important messages that should be
	 *                taken care of.
	 *   c) config - web service configuration & initialization 
     *   d) info   - informative messages
	 */
	public static Logger getLogger(@SuppressWarnings("rawtypes") Class serviceClass) {
		Logger logger = Logger.getLogger(serviceClass.getName());
		logger.addHandler(logDict);
		return logger;
	}
	
	@GET
	@Path("get_log_messages")
	@Produces(MediaType.APPLICATION_JSON)
	public static Map<Level,List<String>> getLogMessages() {
		Map<Level,List<String>> logMessages = logDict.getLogMessages();
		logDict.clear();
		return logMessages;
	}
	
	/**
	 * Print threading and memory information 
	 */
	@GET
	@Path("/meminfo")
	@Produces(MediaType.APPLICATION_JSON)
	public Map<String,Long> meminfo() {
		Map<String, Long> memInfo = new HashMap<>();
		Runtime runtime = Runtime.getRuntime();
		runtime.gc();
		memInfo.put("used", runtime.totalMemory() - runtime.freeMemory());
		memInfo.put("free", runtime.freeMemory());
		memInfo.put("total", runtime.totalMemory());
		memInfo.put("max", runtime.maxMemory());

		// number of running threads
		long runningThreadCount = Thread.getAllStackTraces().size();
		memInfo.put("thread_count", runningThreadCount);
		return memInfo;
	}	

	/**
	 * Print version number
	 */
	@GET
	@Path("/version")
	@Produces(MediaType.APPLICATION_JSON)	
	public String version() {
		String version = null;
		try {
			InputStream stream = context.getResourceAsStream("META-INF/MANIFEST.MF");

			Manifest manifest = new Manifest(stream);
			Attributes attributes = manifest.getMainAttributes();
			version = attributes.getValue("Implementation-Version");
		} catch (IOException e) {
			System.out.println(e.getMessage());
		}
		if (version==null) {
			throw new WeblyzardWebserviceException(
					"Error: There seems to be no 'Implementation-Version' set in the project's META-INF/MANIFEST.MF. "
					+ "Please run mvn war:manifest ... to fix.");
		}
		return version; 
	}
	
 }
