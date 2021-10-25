import numpy as np

from code_base.data_translation_bindings.EU_ISO2_translation import *
from code_base.data_translation_bindings.EU_NUTS3_translation import EU_DECODE_NUTS3_REGIONS
from code_base.data_translation_bindings.age_group_translations import EUROSTAT_AGES_CONVERSION
from code_base.data_translation_bindings.column_naming_consts import COLUMN_HEADING_CONSTS as col_names
from code_base.data_translation_bindings.sex_translations import EUROSTAT_SEX_CONVERSION


class EurostatCleaningParams:
    COLUMN_TO_SPLIT_FROM = {
        'excess_mortality_by_sex_age_country': {
            'demography': 'age,sex,unit,geo\\time',
            'time_period': 'Year_week'
        },
        'excess_mortality_by_sex_age_nuts3': {
            'demography': 'unit,sex,age,geo\\time',
            'time_period': 'Year_week'
        },
        'europe_population_by_age_and_sex': {
            'demography': 'freq;unit;sex;age;geo\TIME_PERIOD'
        },
    }

    COLUMNS_TO_SPLIT_INTO = {
        'excess_mortality_by_sex_age_country': {
            'demography': [col_names.AGE, col_names.SEX, 'Unit', col_names.LOCATION],
            'time_period': [col_names.YEAR, col_names.WEEK],
        },
        'excess_mortality_by_sex_age_nuts3': {
            'demography': ['Unit', col_names.SEX, col_names.AGE, col_names.LOCATION],
            'time_period': [col_names.YEAR, col_names.WEEK],
        },
        'europe_population_by_age_and_sex': {
            'demography': ['Frequency', 'Unit', col_names.SEX, col_names.AGE, col_names.LOCATION]
        },
    }

    COLUMN_SEPARATOR = {
        'excess_mortality_by_sex_age_country': {
            'demography': ',',
            'time_period': 'W',
        },
        'excess_mortality_by_sex_age_nuts3': {
            'demography': ',',
            'time_period': 'W',
        },
        'europe_population_by_age_and_sex': {
            'demography': ';'
        },
    }

    COLUMNS_TO_RETAIN = {
        'excess_mortality_by_sex_age_country': [col_names.AGE, col_names.SEX, col_names.LOCATION],
        'excess_mortality_by_sex_age_nuts3': [col_names.AGE, col_names.SEX, col_names.LOCATION],
        'europe_population_by_age_and_sex': [col_names.AGE, col_names.SEX, col_names.LOCATION, col_names.YEAR_2020],
    }

    TRANSLATE_LOCATION_CODE = {
        'excess_mortality_by_sex_age_country': EU_COUNTRIES_ISO_2_DECODES,
        'excess_mortality_by_sex_age_nuts3': EU_DECODE_NUTS3_REGIONS,
        'europe_population_by_age_and_sex': EU_COUNTRIES_ISO_2_DECODES,
    }

    TRANSLATE_SEX = {
        'excess_mortality_by_sex_age_country': EUROSTAT_SEX_CONVERSION,
        'excess_mortality_by_sex_age_nuts3': EUROSTAT_SEX_CONVERSION,
        'europe_population_by_age_and_sex': EUROSTAT_SEX_CONVERSION,
    }

    TRANSLATE_AGE = {
        'excess_mortality_by_sex_age_country': EUROSTAT_AGES_CONVERSION,
        'excess_mortality_by_sex_age_nuts3': EUROSTAT_AGES_CONVERSION,
        'europe_population_by_age_and_sex': EUROSTAT_AGES_CONVERSION,
    }

    REPLACE_VALUES = [
        ['p', ''],
        [':', np.nan],
        ['e', ''],
    ]
