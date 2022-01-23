from code_base.data_bindings.age_group_translations import UN_DECODE_AGE_GROUPS
from code_base.data_bindings.column_naming_consts import COLUMN_HEADING_CONSTS
from code_base.data_bindings.data_types import LocalDataSets
from code_base.data_bindings.sex_translations import UN_DECODE_SEX_GROUPS, ITALY_DECODE_SEX_GROUPS
from code_base.data_cleaners.cleaning_params import local_cleaning_params as lcp
from code_base.data_cleaners.cleaning_strategies import local_cleaning_strategies


class LocalCleaningConfig:
    AVAILABLE_DATASETS = {
        LocalDataSets.UNDATA_Population,
        LocalDataSets.Italy_Population,
        LocalDataSets.CVD_Europe,
    }

    CLEANING_STRATEGIES = {
        LocalDataSets.UNDATA_Population: local_cleaning_strategies.UnPopulationCleaningStategy,
        LocalDataSets.Italy_Population: local_cleaning_strategies.ItalyPopulationCleaningStategy,
        LocalDataSets.CVD_Europe: local_cleaning_strategies.CVDsEuropeCleaningStategy,
    }

    COLUMNS_TO_RETAIN = {
        LocalDataSets.UNDATA_Population: [lcp.UnDataHeaders.LOCATION_PRE,
                                          lcp.UnDataHeaders.SEX,
                                          lcp.UnDataHeaders.AGE,
                                          lcp.UnDataHeaders.POPULATION_PRE,
                                          lcp.UnDataHeaders.AREA],

        LocalDataSets.Italy_Population: [lcp.ItalyPopDataHeaders.AGE,
                                         lcp.ItalyPopDataHeaders.MEN,
                                         lcp.ItalyPopDataHeaders.WOMEN,
                                         lcp.ItalyPopDataHeaders.TOTAL],

        LocalDataSets.CVD_Europe: [lcp.CVDsEuropeHeaders.Location,
                                   lcp.CVDsEuropeHeaders.Deaths_Raw,
                                   lcp.CVDsEuropeHeaders.Share_Total,
                                   lcp.CVDsEuropeHeaders.Share_Men,
                                   lcp.CVDsEuropeHeaders.Share_Women,
                                   lcp.CVDsEuropeHeaders.Standardized_total,
                                   lcp.CVDsEuropeHeaders.Standardized_Men,
                                   lcp.CVDsEuropeHeaders.Standardized_Women,
                                   lcp.CVDsEuropeHeaders.Standardized_LT65,
                                   lcp.CVDsEuropeHeaders.Standardized_GTE65]
    }

    COLUMNS_TO_RENAME = {
        LocalDataSets.UNDATA_Population: {
            lcp.UnDataHeaders.LOCATION_PRE: COLUMN_HEADING_CONSTS.LOCATION,
            lcp.UnDataHeaders.POPULATION_PRE: COLUMN_HEADING_CONSTS.POPULATION,
        },
        LocalDataSets.Italy_Population: {
            lcp.ItalyPopDataHeaders.AGE: COLUMN_HEADING_CONSTS.AGE,
        },
        LocalDataSets.CVD_Europe: {
            lcp.CVDsEuropeHeaders.Translate_Location:           lcp.CVDsEuropeHeaders.Location,
            lcp.CVDsEuropeHeaders.Translate_Deaths_Raw:         lcp.CVDsEuropeHeaders.Deaths_Raw,
            lcp.CVDsEuropeHeaders.Translate_Share_Total:        lcp.CVDsEuropeHeaders.Share_Total,
            lcp.CVDsEuropeHeaders.Translate_Share_Men:          lcp.CVDsEuropeHeaders.Share_Men,
            lcp.CVDsEuropeHeaders.Translate_Share_Women:        lcp.CVDsEuropeHeaders.Share_Women,
            lcp.CVDsEuropeHeaders.Translate_Standardized_Total: lcp.CVDsEuropeHeaders.Standardized_total,
            lcp.CVDsEuropeHeaders.Translate_Standardized_Men:   lcp.CVDsEuropeHeaders.Standardized_Men,
            lcp.CVDsEuropeHeaders.Translate_Standardized_Women: lcp.CVDsEuropeHeaders.Standardized_Women,
            lcp.CVDsEuropeHeaders.Translate_Standardized_LT65:  lcp.CVDsEuropeHeaders.Standardized_LT65,
            lcp.CVDsEuropeHeaders.Translate_Standardized_GTE65: lcp.CVDsEuropeHeaders.Standardized_GTE65,

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
        return LocalCleaningConfig.COLUMNS_TO_RENAME.get(self._data_type)

    def _get_columns_to_retain(self):
        return LocalCleaningConfig.COLUMNS_TO_RETAIN.get(self._data_type)

    def _get_columns_to_translate(self):
        return LocalCleaningConfig.COLUMNS_TO_TRANSLATE.get(self._data_type)

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
        return LocalCleaningConfig.CLEANING_STRATEGIES[self._data_type]
