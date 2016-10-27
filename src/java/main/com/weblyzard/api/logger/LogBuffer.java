package com.weblyzard.api.logger;

import java.util.concurrent.CopyOnWriteArrayList;

/**
 * A buffer that stores the latest <code>bufferSize</code> elements.
 * @author albert
 *
 * @param <E>
 */
public class LogBuffer<E> extends CopyOnWriteArrayList<E> {
	
	private static final long serialVersionUID = 1L;
	private int bufferSize;
	
	/**
	 * @param size the LogBuffer's size
	 */
	public LogBuffer(int size) {
		super();
		bufferSize = size;
	}
	
	@Override
	public boolean add(E obj) {
		super.add(obj);
		// remove the oldest element from the buffer, if required
		if (this.size() > bufferSize) {
			this.remove(0);
		}
		return true;
	}

}
