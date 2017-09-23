package com.weblyzard.api.model;

/** @author Norman Suesstrunk */
public enum Lang {
    DE,
    EN,
    FR,
    CS,
    ES,
    IT,
    AF,
    AR,
    BG,
    BN,
    DA,
    EL,
    ET,
    FA,
    FI,
    GU,
    HE,
    HI,
    HR,
    HU,
    ID,
    JA,
    KN,
    KO,
    LT,
    LV,
    MK,
    ML,
    MR,
    NE,
    NL,
    NO,
    PA,
    PL,
    PT,
    RO,
    RU,
    SK,
    SL,
    SO,
    SQ,
    SV,
    SW,
    TA,
    TE,
    TH,
    TL,
    TR,
    UK,
    UR,
    VI;

    /**
     * @param lang
     * @return the Lang constant for the given language string (case insensitive)
     */
    public static Lang getLanguage(String lang) {
        return valueOf(lang.toUpperCase());
    }

    @Override
    public String toString() {
        return name().toLowerCase();
    }
}
