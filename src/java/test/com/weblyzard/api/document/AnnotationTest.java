package com.weblyzard.api.document;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNull;

import java.util.Arrays;

import org.junit.Test;

import com.weblyzard.api.document.annotation.Annotation;

public class AnnotationTest {

	/**
	 * This test has been moved from Jeremia
	 */
	@Test
	public void testConstructors() {
		final Annotation lcd1 = new Annotation();
		final Annotation lcd2 = new Annotation("LCD data panel", 672, 686);
		final Annotation lcd3 = new Annotation("LCD data panel", 672, 686, "Product_Feature");
		lcd1.setSurfaceForm( "LCD data panel" );
		lcd1.setStart(672);
		lcd1.setEnd( 686 );
		lcd1.setAnnotationType("Product_Feature");
		lcd2.setAnnotationType("Product_Feature");
		
		for (Annotation lcd: Arrays.asList(lcd1, lcd2, lcd3)) {
			assertEquals("LCD data panel", lcd.getSurfaceForm());
			assertEquals(672, lcd.getStart());
			assertEquals(686, lcd.getEnd());
			assertEquals("Product_Feature", lcd.getAnnotationType());
			assertNull(lcd.getPos());
		}
	}

}
