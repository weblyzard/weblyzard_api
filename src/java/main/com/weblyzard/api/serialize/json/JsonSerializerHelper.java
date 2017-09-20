package com.weblyzard.api.serialize.json;

import java.lang.reflect.Field;
import java.util.Arrays;
import java.util.List;

public class JsonSerializerHelper {

  private JsonSerializerHelper() {}

  public static Iterable<Field> getFieldsUpTo(Class<?> startClass, Class<?> exclusiveParent) {

    List<Field> currentClassFields = Arrays.asList(startClass.getDeclaredFields());
    Class<?> parentClass = startClass.getSuperclass();

    if (parentClass != null
        && (exclusiveParent == null || !(parentClass.equals(exclusiveParent)))) {
      List<Field> parentClassFields = (List<Field>) getFieldsUpTo(parentClass, exclusiveParent);
      currentClassFields.addAll(parentClassFields);
    }

    return currentClassFields;
  }
}
