from code_base.data_bindings.age_group_translations import UN_DECODE_AGE_GROUPS
from code_base.data_bindings.column_naming_consts import COLUMN_HEADING_CONSTS
from code_base.data_bindings.data_types import LocalDataSets
from code_base.data_bindings.sex_translations import UN_DECODE_SEX_GROUPS, ITALY_DECODE_SEX_GROUPS
from code_base.data_cleaners.cleaning_params.local_cleaning_params import UnDataHeaders, ItalyPopDataHeaders
from code_base.data_cleaners.cleaning_strategies import local_cleaning_strategies


class LocalCleaningConfig:
    AVAILABLE_DATASETS = {
        LocalDataSets.UNDATA_Population,
        LocalDataSets.Italy_Population,
    }

    CLEANING_STRATEGIES = {
        LocalDataSets.UNDATA_Population: local_cleaning_strategies.UnPopulationCleaningStategy,
        LocalDataSets.Italy_Population: local_cleaning_strategies.ItalyPopulationCleaningStategy,
    }

    COLUMNS_TO_RETAIN = {
        LocalDataSets.UNDATA_Population: [UnDataHeaders.LOCATION_PRE,
                                          UnDataHeaders.SEX,
                                          UnDataHeaders.AGE,
                                          UnDataHeaders.POPULATION_PRE,
                                          UnDataHeaders.AREA],

        LocalDataSets.Italy_Population: [ItalyPopDataHeaders.AGE,
                                         ItalyPopDataHeaders.MEN,
                                         ItalyPopDataHeaders.WOMEN,
                                         ItalyPopDataHeaders.TOTAL],
    }

    COLUMNS_TO_RENAME = {
        LocalDataSets.UNDATA_Population: {
            UnDataHeaders.LOCATION_PRE:   COLUMN_HEADING_CONSTS.LOCATION,
            UnDataHeaders.POPULATION_PRE: COLUMN_HEADING_CONSTS.POPULATION,
        },
        LocalDataSets.Italy_Population: {
            ItalyPopDataHeaders.AGE:   COLUMN_HEADING_CONSTS.AGE,
            # ItalyPopDataHeaders.MEN :   COLUMN_HEADING_CONSTS.MALE_EN,
            # ItalyPopDataHeaders.WOMEN : COLUMN_HEADING_CONSTS.FEMALE_EN,
            # ItalyPopDataHeaders.TOTAL : COLUMN_HEADING_CONSTS.TOTAL,
        }
    }

    COLUMNS_TO_TRANSLATE = {
        LocalDataSets.UNDATA_Population: {
            COLUMN_HEADING_CONSTS.AGE: UN_DECODE_AGE_GROUPS,
            COLUMN_HEADING_CONSTS.SEX: UN_DECODE_SEX_GROUPS,
        },
        LocalDataSets.Italy_Population: {
            COLUMN_HEADING_CONSTS.SEX: ITALY_DECODE_SEX_GROUPS
        }
    }


class LocalFilesCleaningInfo:

    def __init__(self, data_type):

        self._data_type = data_type

    def _get_columns_to_rename(self):
        return LocalCleaningConfig.COLUMNS_TO_RENAME[self._data_type]

    def _get_columns_to_retain(self):
        return LocalCleaningConfig.COLUMNS_TO_RETAIN[self._data_type]

    def _get_columns_to_translate(self):
        return LocalCleaningConfig.COLUMNS_TO_TRANSLATE[self._data_type]

    def cleaning_params(self, **kwargs):
        retain = self._get_columns_to_retain()
        rename = self._get_columns_to_rename()
        translate = self._get_columns_to_translate()

        cleaning_params = {
            'columns_to_retain': retain,
            'columns_to_rename': rename,
            'translate_values':  translate
        }

        return cleaning_params

    @property
    def cleaning_strategy(self):
        return LocalCleaningConfig.CLEANING_STRATEGIES[self._data_type]