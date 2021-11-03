import numpy as np

from code_base.data_bindings.EU_ISO2_translation import *
from code_base.data_bindings.EU_NUTS3_translation import EU_DECODE_NUTS3_REGIONS
from code_base.data_bindings.age_group_translations import EUROSTAT_AGES_CONVERSION
from code_base.data_bindings.column_naming_consts import COLUMN_HEADING_CONSTS as COL_HEADER
from code_base.data_bindings.data_types import EurostatDataSets as DtTp
from code_base.data_bindings.sex_translations import EUROSTAT_SEX_CONVERSION


class EurostatCleaningParams:
    COLUMN_TO_SPLIT_FROM = {
        DtTp.MORTALITY_BY_SEX_AGE_COUNTRY: {
            'demography': 'age,sex,unit,geo\\time',
            'time_period': 'Year_week'
        },
        DtTp.MORTALITY_BY_SEX_AGE_REGION: {
            'demography': 'unit,sex,age,geo\\time',
            'time_period': 'Year_week'
        },
        DtTp.POP_BY_SEX_AGE_COUNTRY: {
            'demography': 'freq;unit;sex;age;geo\TIME_PERIOD'
        },
    }

    COLUMNS_TO_SPLIT_INTO = {
        DtTp.MORTALITY_BY_SEX_AGE_COUNTRY: {
            'demography': [COL_HEADER.AGE, COL_HEADER.SEX, 'Unit', COL_HEADER.LOCATION],
            'time_period': [COL_HEADER.YEAR, COL_HEADER.WEEK],
        },
        DtTp.MORTALITY_BY_SEX_AGE_REGION: {
            'demography': ['Unit', COL_HEADER.SEX, COL_HEADER.AGE, COL_HEADER.LOCATION],
            'time_period': [COL_HEADER.YEAR, COL_HEADER.WEEK],
        },
        DtTp.POP_BY_SEX_AGE_COUNTRY: {
            'demography': ['Frequency', 'Unit', COL_HEADER.SEX, COL_HEADER.AGE, COL_HEADER.LOCATION]
        },
    }

    COLUMN_SEPARATOR = {
        DtTp.MORTALITY_BY_SEX_AGE_COUNTRY: {
            'demography': ',',
            'time_period': 'W',
        },
        DtTp.MORTALITY_BY_SEX_AGE_REGION: {
            'demography': ',',
            'time_period': 'W',
        },
        DtTp.POP_BY_SEX_AGE_COUNTRY: {
            'demography': ';'
        },
    }

    COLUMNS_TO_RETAIN = {
        DtTp.MORTALITY_BY_SEX_AGE_COUNTRY: [COL_HEADER.AGE, COL_HEADER.SEX, COL_HEADER.LOCATION],
        DtTp.MORTALITY_BY_SEX_AGE_REGION: [COL_HEADER.AGE, COL_HEADER.SEX, COL_HEADER.LOCATION],
        DtTp.POP_BY_SEX_AGE_COUNTRY: [COL_HEADER.AGE, COL_HEADER.SEX, COL_HEADER.LOCATION, COL_HEADER.YEAR_2020],
    }

    TRANSLATE_LOCATION_CODE = {
        DtTp.MORTALITY_BY_SEX_AGE_COUNTRY: EU_COUNTRIES_ISO_2_DECODES,
        DtTp.MORTALITY_BY_SEX_AGE_REGION: EU_DECODE_NUTS3_REGIONS,
        DtTp.POP_BY_SEX_AGE_COUNTRY: EU_COUNTRIES_ISO_2_DECODES,
    }

    TRANSLATE_SEX = {
        DtTp.MORTALITY_BY_SEX_AGE_COUNTRY: EUROSTAT_SEX_CONVERSION,
        DtTp.MORTALITY_BY_SEX_AGE_REGION: EUROSTAT_SEX_CONVERSION,
        DtTp.POP_BY_SEX_AGE_COUNTRY: EUROSTAT_SEX_CONVERSION,
    }

    TRANSLATE_AGE = {
        DtTp.MORTALITY_BY_SEX_AGE_COUNTRY: EUROSTAT_AGES_CONVERSION,
        DtTp.MORTALITY_BY_SEX_AGE_REGION: EUROSTAT_AGES_CONVERSION,
        DtTp.POP_BY_SEX_AGE_COUNTRY: EUROSTAT_AGES_CONVERSION,
    }

    REPLACE_VALUES = [
        ['p', ''],
        [':', np.nan],
        ['e', ''],
    ]
