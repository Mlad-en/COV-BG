from code_base.data_bindings import age_group_translations
from code_base.data_bindings.column_naming_consts import COLUMN_HEADING_CONSTS
from code_base.data_bindings.data_types import LocalDataSets
from code_base.data_bindings import sex_translations
from code_base.data_cleaners.cleaning_params import local_cleaning_params as lcp
from code_base.data_cleaners.cleaning_strategies import local_cleaning_strategies


class LocalCleaningConfig:
    AVAILABLE_DATASETS = {
        LocalDataSets.UNDATA_POPULATION,
        LocalDataSets.ITALY_POPULATION,
        LocalDataSets.CVD_EUROPE,
    }

    CLEANING_STRATEGIES = {
        LocalDataSets.UNDATA_POPULATION: local_cleaning_strategies.UnPopulationCleaningStategy,
        LocalDataSets.ITALY_POPULATION:  local_cleaning_strategies.ItalyPopulationCleaningStategy,
        LocalDataSets.CVD_EUROPE:        local_cleaning_strategies.CVDsEuropeCleaningStategy,
        LocalDataSets.STD_POPULATION_EU: local_cleaning_strategies.StandardizedEUPopulationCleaningStrategy,
    }

    COLUMNS_TO_RETAIN = {
        LocalDataSets.UNDATA_POPULATION: [lcp.UnDataHeaders.LOCATION_PRE,
                                          lcp.UnDataHeaders.SEX,
                                          lcp.UnDataHeaders.AGE,
                                          lcp.UnDataHeaders.POPULATION_PRE,
                                          lcp.UnDataHeaders.AREA],

        LocalDataSets.ITALY_POPULATION: [lcp.ItalyPopDataHeaders.AGE,
                                         lcp.ItalyPopDataHeaders.MEN,
                                         lcp.ItalyPopDataHeaders.WOMEN,
                                         lcp.ItalyPopDataHeaders.TOTAL],

        LocalDataSets.CVD_EUROPE: [lcp.CVDsEuropeHeaders.Location,
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
        LocalDataSets.UNDATA_POPULATION: {
            lcp.UnDataHeaders.LOCATION_PRE: COLUMN_HEADING_CONSTS.LOCATION,
            lcp.UnDataHeaders.POPULATION_PRE: COLUMN_HEADING_CONSTS.POPULATION,
        },
        LocalDataSets.ITALY_POPULATION: {
            lcp.ItalyPopDataHeaders.AGE: COLUMN_HEADING_CONSTS.AGE,
        },
        LocalDataSets.CVD_EUROPE: {
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
        },
        LocalDataSets.STD_POPULATION_EU: {
            lcp.StandardPopHeaders.Translate_Pop: lcp.StandardPopHeaders.Standardized_Pop
        }
    }

    COLUMNS_TO_TRANSLATE = {
        LocalDataSets.UNDATA_POPULATION: {
            COLUMN_HEADING_CONSTS.AGE: age_group_translations.UN_DECODE_AGE_GROUPS,
            COLUMN_HEADING_CONSTS.SEX: sex_translations.UN_DECODE_SEX_GROUPS,
        },
        LocalDataSets.ITALY_POPULATION: {
            COLUMN_HEADING_CONSTS.SEX: sex_translations.ITALY_DECODE_SEX_GROUPS
        },
        LocalDataSets.STD_POPULATION_EU: {
            COLUMN_HEADING_CONSTS.AGE: age_group_translations.STD_EU_POP_2013_DECODE_AGE
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
