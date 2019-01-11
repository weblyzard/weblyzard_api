package com.weblyzard.api.model;

import java.util.Optional;

/**
 * Language codes supported by the webLyzard API.
 * 
 * @author Norman Suesstrunk
 */
public enum Lang {
    ANY, DE, EN, FR, CS, ES, IT, AF, AR, BG, BN, DA, EL, ET, FA, FI, GU, HE, HI, HR, HU, ID, IS, JA, KN, KO, LT, LV, MK, ML, MR, NE, NL, NO, PA, PL, PT, RO, RU, SK, SL, SO, SQ, SV, SW, TA, TE, TH, TL, TR, UK, UR, VI;

    /**
     * Transforms a String with a language code into the corresponding Lang Enum.
     * 
     * @param lang language String to be converted to a constant
     * @return the Lang constant for the given language string (case insensitive)
     */
    public static Optional<Lang> getLanguage(String lang) {
        try {
            return Optional.of(valueOf(lang.toUpperCase()));
        } catch (NullPointerException | IllegalArgumentException e) {
            return Optional.empty();
        }
    }

    @Override
    public String toString() {
        return name().toLowerCase();
    }
}
