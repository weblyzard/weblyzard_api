package com.weblyzard.api.logger;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.logging.Handler;
import java.util.logging.Level;
import java.util.logging.LogRecord;
import java.util.logging.SimpleFormatter;
/**
 * Logs events to a dictionary object
 * @author Albert Weichselbraun <albert.weichselbraun@htwchur.ch>
 *
 */
public class DictionaryLogHandler extends Handler {
	private int bufferSize;
	private Map<Level,List<String>> logMessages;
	
	public DictionaryLogHandler(int bufferSize) {
		super();
		this.bufferSize = bufferSize;
		setFormatter(new SimpleFormatter());
		clear();
	}

	/**
	 * Re-initializes the dictionary log..
	 */
	public void clear() {
		logMessages = new HashMap<>();
		logMessages.put(Level.FINEST, new LogBuffer<String>(bufferSize));
		logMessages.put(Level.FINER, new LogBuffer<String>(bufferSize));
		logMessages.put(Level.FINE, new LogBuffer<String>(bufferSize));
		logMessages.put(Level.CONFIG, new LogBuffer<String>(bufferSize));
		logMessages.put(Level.INFO, new LogBuffer<String>(bufferSize));
		logMessages.put(Level.WARNING, new LogBuffer<String>(bufferSize));
		logMessages.put(Level.SEVERE, new LogBuffer<String>(bufferSize));
	}

	public void setLogBufferSize(int size) { bufferSize = size; clear(); }
	
	public Map<Level,List<String>> getLogMessages() { 
		return logMessages; 
	}
	
	@Override
	public void publish(LogRecord record) {
		if (!isLoggable(record)) {
			return;
		}
		logMessages.get(record.getLevel()).add(getFormatter().format(record));
	}
	
	@Override
	public void close() throws SecurityException {}

	@Override
	public void flush() {}
	
}
