class AGE_BINDINGS:

    TOTAL = 'Total'
    AGE_00_04 = '(0-4)'
    AGE_05_09 = '(5-9)'
    AGE_10_14 = '(10-14)'
    AGE_15_19 = '(15-19)'
    AGE_20_24 = '(20-24)'
    AGE_25_29 = '(25-29)'
    AGE_30_34 = '(30-34)'
    AGE_35_39 = '(35-39)'
    AGE_40_44 = '(40-44)'
    AGE_45_49 = '(45-49)'
    AGE_50_54 = '(50-54)'
    AGE_55_59 = '(55-59)'
    AGE_60_64 = '(60-64)'
    AGE_65_69 = '(65-69)'
    AGE_70_74 = '(70-74)'
    AGE_75_79 = '(75-79)'
    AGE_80_84 = '(80-84)'
    AGE_85_89 = '(85-89)'
    AGE_GE90 = '(90+)'


EUROSTAT_AGES_CONVERSION = {
    'TOTAL':  AGE_BINDINGS.TOTAL,
    'Y_LT5':  AGE_BINDINGS.AGE_00_04,
    'Y5-9':   AGE_BINDINGS.AGE_05_09,
    'Y10-14': AGE_BINDINGS.AGE_10_14,
    'Y15-19': AGE_BINDINGS.AGE_15_19,
    'Y20-24': AGE_BINDINGS.AGE_20_24,
    'Y25-29': AGE_BINDINGS.AGE_25_29,
    'Y30-34': AGE_BINDINGS.AGE_30_34,
    'Y35-39': AGE_BINDINGS.AGE_35_39,
    'Y40-44': AGE_BINDINGS.AGE_40_44,
    'Y45-49': AGE_BINDINGS.AGE_45_49,
    'Y50-54': AGE_BINDINGS.AGE_50_54,
    'Y55-59': AGE_BINDINGS.AGE_55_59,
    'Y60-64': AGE_BINDINGS.AGE_60_64,
    'Y65-69': AGE_BINDINGS.AGE_65_69,
    'Y70-74': AGE_BINDINGS.AGE_70_74,
    'Y75-79': AGE_BINDINGS.AGE_75_79,
    'Y80-84': AGE_BINDINGS.AGE_80_84,
    'Y85-89': AGE_BINDINGS.AGE_85_89,
    'Y_GE90': AGE_BINDINGS.AGE_GE90,
}

UN_DECODE_AGE_GROUPS = {
    'Total':   AGE_BINDINGS.TOTAL,
    '0 - 4':   AGE_BINDINGS.AGE_00_04,
    '5 - 9':   AGE_BINDINGS.AGE_05_09,
    '10 - 14': AGE_BINDINGS.AGE_10_14,
    '15 - 19': AGE_BINDINGS.AGE_15_19,
    '20 - 24': AGE_BINDINGS.AGE_20_24,
    '25 - 29': AGE_BINDINGS.AGE_25_29,
    '30 - 34': AGE_BINDINGS.AGE_30_34,
    '35 - 39': AGE_BINDINGS.AGE_35_39,
    '40 - 44': AGE_BINDINGS.AGE_40_44,
    '45 - 49': AGE_BINDINGS.AGE_45_49,
    '50 - 54': AGE_BINDINGS.AGE_50_54,
    '55 - 59': AGE_BINDINGS.AGE_55_59,
    '60 - 64': AGE_BINDINGS.AGE_60_64,
    '65 - 69': AGE_BINDINGS.AGE_65_69,
    '70 - 74': AGE_BINDINGS.AGE_70_74,
    '75 - 79': AGE_BINDINGS.AGE_75_79,
    '80 - 84': AGE_BINDINGS.AGE_80_84,
    '85 - 89': AGE_BINDINGS.AGE_85_89,
    '90 - 94': AGE_BINDINGS.AGE_GE90,
    '95 - 99': AGE_BINDINGS.AGE_GE90,
    '100 +':   AGE_BINDINGS.AGE_GE90,
    '90 +':    AGE_BINDINGS.AGE_GE90,

}

std_eu_pop_2013_decode_age = {
    # Combine 0-4 by decoding under 1 and 1-4 as the same value
    'Under 1 year':            AGE_BINDINGS.AGE_00_04,
    '1 year to under 5 years': AGE_BINDINGS.AGE_00_04,
    '5 to under 10 years':     AGE_BINDINGS.AGE_05_09,
    '10 to under 15 years':    AGE_BINDINGS.AGE_10_14,
    '15 to under 20 years':    AGE_BINDINGS.AGE_15_19,
    '20 to under 25 years':    AGE_BINDINGS.AGE_20_24,
    '25 to under 30 years':    AGE_BINDINGS.AGE_25_29,
    '30 to under 35 years':    AGE_BINDINGS.AGE_30_34,
    '35 to under 40 years':    AGE_BINDINGS.AGE_35_39,
    '40 to under 45 years':    AGE_BINDINGS.AGE_40_44,
    '45 to under 50 years':    AGE_BINDINGS.AGE_45_49,
    '50 to under 55 years':    AGE_BINDINGS.AGE_50_54,
    '55 to under 60 years':    AGE_BINDINGS.AGE_55_59,
    '60 to under 65 years':    AGE_BINDINGS.AGE_60_64,
    '65 to under 70 years':    AGE_BINDINGS.AGE_65_69,
    '70 to under 75 years':    AGE_BINDINGS.AGE_70_74,
    '75 to under 80 years':    AGE_BINDINGS.AGE_75_79,
    '80 to under 85 years':    AGE_BINDINGS.AGE_80_84,
    '85 to under 90 years':    AGE_BINDINGS.AGE_85_89,
    '90 years and older':      AGE_BINDINGS.AGE_GE90,
}

INFOSTAT_DECODE_AGE_GROUPS = {
    'Total': AGE_BINDINGS.TOTAL,
    # Combine 0-4 by decoding under 1 and 1-4 as the same value
    '0':       AGE_BINDINGS.AGE_00_04,
    '1 - 4':   AGE_BINDINGS.AGE_00_04,
    '5 - 9':   AGE_BINDINGS.AGE_05_09,
    '10 - 14': AGE_BINDINGS.AGE_10_14,
    '15 - 19': AGE_BINDINGS.AGE_15_19,
    '20 - 24': AGE_BINDINGS.AGE_20_24,
    '25 - 29': AGE_BINDINGS.AGE_25_29,
    '30 - 34': AGE_BINDINGS.AGE_30_34,
    '35 - 39': AGE_BINDINGS.AGE_35_39,
    '40 - 44': AGE_BINDINGS.AGE_40_44,
    '45 - 49': AGE_BINDINGS.AGE_45_49,
    '50 - 54': AGE_BINDINGS.AGE_50_54,
    '55 - 59': AGE_BINDINGS.AGE_55_59,
    '60 - 64': AGE_BINDINGS.AGE_60_64,
    '65 - 69': AGE_BINDINGS.AGE_65_69,
    '70 - 74': AGE_BINDINGS.AGE_70_74,
    '75 - 79': AGE_BINDINGS.AGE_75_79,
    '80 - 84': AGE_BINDINGS.AGE_80_84,
    '85 - 89': AGE_BINDINGS.AGE_85_89,
    '90 - 94': AGE_BINDINGS.AGE_GE90,
    '95 - 99': AGE_BINDINGS.AGE_GE90,
    '100+': AGE_BINDINGS.AGE_GE90,
}
