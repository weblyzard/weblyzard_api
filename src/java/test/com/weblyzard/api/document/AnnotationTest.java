package com.weblyzard.api.document;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNull;

import com.weblyzard.api.model.annotation.Annotation;
import java.util.Arrays;
import org.junit.Test;

public class AnnotationTest {

    /** This test has been moved from Jeremia */
    @Test
    public void testConstructors() {
        final Annotation lcd1 = new Annotation();
        final Annotation lcd2 =
                Annotation.build("http://dbpedia.org/lcd_data_panel")
                        .setSurfaceForm("LCD data panel")
                        .setStart(672)
                        .setEnd(686)
                        .setSentence(0);
        final Annotation lcd3 =
                Annotation.build("http://dbpedia.org/lcd_data_panel")
                        .setSurfaceForm("LCD data panel")
                        .setStart(672)
                        .setEnd(686)
                        .setSentence(0)
                        .setEntityType("Product_Feature")
                        .annotation();

        lcd1.setSurfaceForm("LCD data panel");
        lcd1.setStart(672);
        lcd1.setEnd(686);
        lcd1.setEntityType("Product_Feature");
        lcd2.setEntityType("Product_Feature");

        for (Annotation lcd : Arrays.asList(lcd1, lcd2, lcd3)) {
            assertEquals("LCD data panel", lcd.getSurfaceForm());
            assertEquals(672, lcd.getStart());
            assertEquals(686, lcd.getEnd());
            assertEquals("Product_Feature", lcd.getEntityType());
            assertNull(lcd.getPos());
        }
    }
}
