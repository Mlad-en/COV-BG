from code_base.data_bindings.EU_ISO3_TRANSLATIONS import EU_COUNTRIES_ISO_3_DECODES
from code_base.data_bindings.age_group_translations import WHOInt_DECODE_AGE_GROUPS
from code_base.data_bindings.column_naming_consts import COLUMN_HEADING_CONSTS
from code_base.data_bindings.data_types import WHODataSets
from code_base.data_bindings.sex_translations import WHO_SEX_CONVERSION
from code_base.data_cleaners.cleaning_strategies.who_cleaning_strategies import WHoLifeExpectancyCleaningStrategy


class WHOCleaningConfig:
    AVAILABLE_DATASETS = {
        WHODataSets.LIFE_EXPECTANCY_BY_AGE_SEX,
    }

    CLEANING_STRATEGIES = {
        WHODataSets.LIFE_EXPECTANCY_BY_AGE_SEX: WHoLifeExpectancyCleaningStrategy,
    }

    COLUMNS_TO_RETAIN = {
        WHODataSets.LIFE_EXPECTANCY_BY_AGE_SEX: ['YEAR', 'COUNTRY', 'AGEGROUP', 'SEX', 'Numeric'],
    }

    COLUMNS_TO_RENAME = {
        WHODataSets.LIFE_EXPECTANCY_BY_AGE_SEX: {
            'YEAR':     COLUMN_HEADING_CONSTS.YEAR,
            'COUNTRY':  COLUMN_HEADING_CONSTS.LOCATION,
            'AGEGROUP': COLUMN_HEADING_CONSTS.AGE,
            'SEX':      COLUMN_HEADING_CONSTS.SEX,
            'Numeric':  COLUMN_HEADING_CONSTS.LIFE_EXPECTANCY,
        }
    }

    COLUMNS_TO_TRANSLATE = {
        WHODataSets.LIFE_EXPECTANCY_BY_AGE_SEX: {
            COLUMN_HEADING_CONSTS.LOCATION: EU_COUNTRIES_ISO_3_DECODES,
            COLUMN_HEADING_CONSTS.AGE:      WHOInt_DECODE_AGE_GROUPS,
            COLUMN_HEADING_CONSTS.SEX:      WHO_SEX_CONVERSION,
        }
    }


class WHOCleaningInfo:

    def __init__(self, data_type):

        self._data_type = data_type

    def _get_columns_to_rename(self):
        return WHOCleaningConfig.COLUMNS_TO_RENAME[self._data_type]

    def _get_columns_to_retain(self):
        return WHOCleaningConfig.COLUMNS_TO_RETAIN[self._data_type]

    def _get_columns_to_translate(self):
        return WHOCleaningConfig.COLUMNS_TO_TRANSLATE[self._data_type]

    def cleaning_params(self, **kwargs):
        retain = self._get_columns_to_retain()
        rename = self._get_columns_to_rename()
        translate = self._get_columns_to_translate()

        cleaning_params = {
            'columns_to_retain': retain,
            'columns_to_rename': rename,
            'translate_values': translate
        }

        return cleaning_params

    @property
    def cleaning_strategy(self):
        return WHOCleaningConfig.CLEANING_STRATEGIES[self._data_type]
