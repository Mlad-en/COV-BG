from code_base.excess_mortality.decode_loc_vars import *

DECODE_DEMO_COL = {
    'excess_mortality_by_sex_age_country': 'age,sex,unit,geo\\time',
    'excess_mortality_by_sex_age_nuts3': 'unit,sex,age,geo\\time',
    'europe_population_by_age_and_sex': 'freq;unit;sex;age;geo\TIME_PERIOD'
}

DECODE_DEMO_REPL = {
    'excess_mortality_by_sex_age_country': ['Age', 'Sex', 'Unit', 'Location'],
    'excess_mortality_by_sex_age_nuts3': ['Unit', 'Sex', 'Age', 'Location'],
    'europe_population_by_age_and_sex': ['Frequency', 'Unit', 'Sex', 'Age', 'Location']
}

RETAIN_COLUMNS = {
    'excess_mortality_by_sex_age_country': ['Age', 'Sex', 'Location'],
    'excess_mortality_by_sex_age_nuts3': ['Age', 'Sex', 'Location'],
    'europe_population_by_age_and_sex': ['2020 ', 'Sex', 'Age', 'Location']
}

COUNTRY_REPLACE = {
    'excess_mortality_by_sex_age_country': EU_COUNTRIES_ISO_2_DECODES,
    'excess_mortality_by_sex_age_nuts3': EU_DECODE_NUTS3_REGIONS,
    'europe_population_by_age_and_sex': EU_COUNTRIES_ISO_2_DECODES
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

UN_DECODE_AGE_GROUPS = {
    'Total': 'Total',
    '0 - 4': '(0-4)',
    '5 - 9': '(5-9)',
    '10 - 14': '(10-14)',
    '15 - 19': '(15-19)',
    '20 - 24': '(20-24)',
    '25 - 29': '(25-29)',
    '30 - 34': '(30-34)',
    '35 - 39': '(35-39)',
    '40 - 44': '(40-44)',
    '45 - 49': '(45-49)',
    '50 - 54': '(50-54)',
    '55 - 59': '(55-59)',
    '60 - 64': '(60-64)',
    '65 - 69': '(65-69)',
    '70 - 74': '(70-74)',
    '75 - 79': '(75-79)',
    '80 - 84': '(80-84)',
    '85 - 89': '(85-89)',
    '90 +': '(90+)',
}

UN_DECODE_SEX_GROUPS = {
    'Both Sexes': 'Total',
    'Male': 'Male',
    'Female': 'Female',
}


std_eu_pop_2013_decode_age = {
    # Todo: Add explanations for 0-4
    'Under 1 year': '(0-4)',
    '1 year to under 5 years': '(0-4)',
    '5 to under 10 years': '(5-9)',
    '10 to under 15 years': '(10-14)',
    '15 to under 20 years': '(15-19)',
    '20 to under 25 years': '(20-24)',
    '25 to under 30 years': '(25-29)',
    '30 to under 35 years': '(30-34)',
    '35 to under 40 years': '(35-39)',
    '40 to under 45 years': '(40-44)',
    '45 to under 50 years': '(45-49)',
    '50 to under 55 years': '(50-54)',
    '55 to under 60 years': '(55-59)',
    '60 to under 65 years': '(60-64)',
    '65 to under 70 years': '(65-69)',
    '70 to under 75 years': '(70-74)',
    '75 to under 80 years': '(75-79)',
    '80 to under 85 years': '(80-84)',
    '85 to under 90 years': '(85-89)',
    '90 years and older': '(90+)',
}