from code_base.data_bindings import cvbg_translate_cols
from code_base.data_bindings.data_types import CoronaVirusBGDataSets
from code_base.data_cleaners.cleaning_strategies import cvbg_cleaning_strategy


class WHOCleaningConfig:
    AVAILABLE_DATASETS = {
        CoronaVirusBGDataSets.GENERAL,
        CoronaVirusBGDataSets.BY_REGION,
        CoronaVirusBGDataSets.BY_AGE_GROUP,
        CoronaVirusBGDataSets.BY_TEST_TYPE,
        CoronaVirusBGDataSets.DECEASED_BY_SEX_AGE,
        CoronaVirusBGDataSets.VACCINATED_INFECTED,
        CoronaVirusBGDataSets.VACCINATED_HOSPITALIZED,
        CoronaVirusBGDataSets.VACCINATED_ICU,
        CoronaVirusBGDataSets.VACCINATED_DECEASED,
    }

    CLEANING_STRATEGIES = {
        CoronaVirusBGDataSets.GENERAL: cvbg_cleaning_strategy.CoronaVirusBGGeneralCleaningStategy,
    }

    COLUMNS_TO_RENAME = {
        CoronaVirusBGDataSets.GENERAL: cvbg_translate_cols.CV_BG_GENERAL_DISTRIBUTION_STATISTICS,
        CoronaVirusBGDataSets.BY_REGION: cvbg_translate_cols.CV_BG_DISTRIBUTION_BY_REGION,
        CoronaVirusBGDataSets.BY_AGE_GROUP: cvbg_translate_cols.CV_BG_DISTRIBUTION_BY_AGE,
        CoronaVirusBGDataSets.BY_TEST_TYPE: cvbg_translate_cols.CV_BG_DISTRIBUTION_BY_TESTS,
        CoronaVirusBGDataSets.DECEASED_BY_SEX_AGE: cvbg_translate_cols.CV_BG_DECEASED_BY_GENDER_SEX,
        CoronaVirusBGDataSets.VACCINATED_INFECTED: cvbg_translate_cols.CV_BG_INFECTED_VACCINATED,
        CoronaVirusBGDataSets.VACCINATED_HOSPITALIZED: cvbg_translate_cols.CV_BG_HOSPITALIZED_VACCINATED,
        CoronaVirusBGDataSets.VACCINATED_ICU: cvbg_translate_cols.CV_BG_ICU_VACCINATED,
        CoronaVirusBGDataSets.VACCINATED_DECEASED: cvbg_translate_cols.CV_BG_DECEASED_VACCINATED,
    }

    COLUMNS_TO_RETAIN = {
        CoronaVirusBGDataSets.GENERAL: [],
    }


class CVBGCleaningInfo:

    def __init__(self, data_type):

        self._data_type = data_type

    def _get_columns_to_rename(self):
        return WHOCleaningConfig.COLUMNS_TO_RENAME[self._data_type]

    def cleaning_params(self, **kwargs):
        rename = self._get_columns_to_rename()

        cleaning_params = {
            'columns_to_rename': rename,
        }

        return cleaning_params

    @property
    def cleaning_strategy(self):
        return WHOCleaningConfig.CLEANING_STRATEGIES[self._data_type]