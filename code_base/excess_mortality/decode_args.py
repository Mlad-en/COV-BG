from code_base.excess_mortality.decode_loc_vars import *

DECODE_DEMO_COL = {
    'excess_mortality_by_sex_age_country': 'age,sex,unit,geo\\time',
    'excess_mortality_by_sex_age_nuts3': 'unit,sex,age,geo\\time',
}

DECODE_DEMO_REPL = {
    'excess_mortality_by_sex_age_country': ['Age', 'Sex', 'Unit', 'Location'],
    'excess_mortality_by_sex_age_nuts3': ['Unit', 'Sex', 'Age', 'Location'],
}

RETAIN_COLUMNS = {
    'excess_mortality_by_sex_age_country': ['Age', 'Sex', 'Location'],
    'excess_mortality_by_sex_age_nuts3': ['Age', 'Sex', 'Location'],
}

COUNTRY_REPLACE = {
    'excess_mortality_by_sex_age_country': EU_COUNTRIES_ISO_2_DECODES,
    'excess_mortality_by_sex_age_nuts3': EU_DECODE_NUTS3_REGIONS,
}

FILE_EXT_TYPE = {
    'csv': '.csv',
    'latex': '.tex',
    'excel': '.xlsx',
    'pickle': '.pickle'
}

EUROSTAT_AGES_CONVERSION = {
    'TOTAL': 'Total',
    'Y_LT5': '(0-4)',
    'Y5-9': '(5-9)',
    'Y10-14': '(10-14)',
    'Y15-19': '(15-19)',
    'Y20-24': '(20-24)',
    'Y25-29': '(25-29)',
    'Y30-34': '(30-34)',
    'Y35-39': '(35-39)',
    'Y40-44': '(40-44)',
    'Y45-49': '(45-49)',
    'Y50-54': '(50-54)',
    'Y55-59': '(55-59)',
    'Y60-64': '(60-64)',
    'Y65-69': '(65-69)',
    'Y70-74': '(70-74)',
    'Y75-79': '(75-79)',
    'Y80-84': '(80-84)',
    'Y85-89': '(85-89)',
    'Y_GE90': '(90+)',
}

EUROSTAT_SEX_CONVERSION = {
    'F': 'Female',
    'M': 'Male',
    'T': 'Total',
}
