/**
 * {@link com.weblyzard.api.model.annotation.Annotation}s to be used in conjunction with the {@link
 * com.weblyzard.api.model.document.Document} class.
 *
 * <p>The API distinguishes between two Annotation types:
 *
 * <ul>
 *   <li>{@link com.weblyzard.api.model.annotation.Annotation} which includes the {@link
 *       com.weblyzard.api.model.annotation.EntityDescriptor} and the entity's location within a
 *       {@link com.weblyzard.api.model.document.Document}.
 *   <li>{@link com.weblyzard.api.model.annotation.CompactAnnotation} that contains the {@link
 *       com.weblyzard.api.model.annotation.EntityDescriptor} and a list of {@link
 *       com.weblyzard.api.model.annotation.AnnotationSurface}s, each referencing one appearance in
 *       the {@link com.weblyzard.api.model.document.Document}
 * </ul>
 */
package com.weblyzard.api.model.annotation;
