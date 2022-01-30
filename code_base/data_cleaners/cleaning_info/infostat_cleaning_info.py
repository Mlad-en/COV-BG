from typing import List

from code_base.data_bindings.data_types import InfostatDataSets as DtTp
from code_base.data_cleaners.cleaning_params.infostat_params import InfostatHeaders, InfostatCleaningParams
from code_base.data_cleaners.cleaning_strategies.infostat_cleaning_strategies import *


class InfostatConfig:
    AVAILABLE_DATASETS = {
        DtTp.POP_BY_SEX_AGE_REG,
        DtTp.AVG_LIFE_EXPECTANCY_BY_SEX,
        DtTp.LIFE_EXPECTANCY_BY_SEX,
        DtTp.MORTALITY_BY_SEX_AGE_MUN,
        DtTp.POP_BY_MUNICIPALITY,
    }

    FILTER_DF_BY = {
        DtTp.POP_BY_SEX_AGE_REG: [InfostatHeaders.FEMALE_EN, InfostatHeaders.MALE_EN],
        DtTp.AVG_LIFE_EXPECTANCY_BY_SEX: [InfostatHeaders.FEMALE_EN, InfostatHeaders.MALE_EN],
        DtTp.LIFE_EXPECTANCY_BY_SEX: [InfostatHeaders.FEMALE_EN, InfostatHeaders.MALE_EN],
        DtTp.MORTALITY_BY_SEX_AGE_MUN: [InfostatHeaders.FEMALE_BG, InfostatHeaders.MALE_BG],
        DtTp.POP_BY_MUNICIPALITY: [InfostatHeaders.FEMALE_BG, InfostatHeaders.MALE_BG],
    }

    INFOSTAT_CLEANING_STRATEGY = {
        DtTp.POP_BY_SEX_AGE_REG: PopulationAgeSexRegionCleaningStrategy,
        DtTp.AVG_LIFE_EXPECTANCY_BY_SEX: AVGLifeExpectancyBySexCleaningStrategy,
        DtTp.LIFE_EXPECTANCY_BY_SEX: LifeExpectancyBySexCleaningStrategy,
        DtTp.MORTALITY_BY_SEX_AGE_MUN: MortalityByAgeSexMunicipalityCleaningStrategy,
        DtTp.POP_BY_MUNICIPALITY: PopulationByMunicipalityCleaningStrategy,
    }

    INFOSTAT_INIT_COLUMNS = {
        DtTp.POP_BY_SEX_AGE_REG: InfostatCleaningParams.cols_pop_by_age_sex_reg(),
        DtTp.AVG_LIFE_EXPECTANCY_BY_SEX: InfostatCleaningParams.cols_avg_life_expectancy_by_sex(),
        DtTp.LIFE_EXPECTANCY_BY_SEX: InfostatCleaningParams.cols_life_expectancy_by_sex(),
        DtTp.MORTALITY_BY_SEX_AGE_MUN: InfostatCleaningParams.cols_mortality_by_age_sex_mun(),
        DtTp.POP_BY_MUNICIPALITY: InfostatCleaningParams.cols_population_by_municipality(),
    }

    MELT_COLS = {
        DtTp.POP_BY_SEX_AGE_REG: {'id_vars': [InfostatHeaders.LOCATION, InfostatHeaders.AGE],
                                  'var_name': InfostatHeaders.SEX,
                                  'value_name': InfostatHeaders.POPULATION},

        DtTp.AVG_LIFE_EXPECTANCY_BY_SEX: {'id_vars': [InfostatHeaders.LOCATION],
                                          'var_name': InfostatHeaders.SEX,
                                          'value_name': InfostatHeaders.LIFE_EXPECTANCY},

        DtTp.LIFE_EXPECTANCY_BY_SEX: {'id_vars': [InfostatHeaders.AGE],
                                      'var_name': InfostatHeaders.SEX,
                                      'value_name': InfostatHeaders.LIFE_EXPECTANCY},

        DtTp.MORTALITY_BY_SEX_AGE_MUN: {'id_vars': [InfostatHeaders.LOCATION],
                                        'var_name': InfostatHeaders.YEAR_SEX,
                                        'value_name': InfostatHeaders.MORTALITY},

        DtTp.POP_BY_MUNICIPALITY: {'id_vars': [InfostatHeaders.LOCATION],
                                   'var_name': InfostatHeaders.SEX,
                                   'value_name': InfostatHeaders.POPULATION},
    }

    SHARED_CLEANING_PARAMS = {
        'filter_df_by': FILTER_DF_BY,
        'col_headers': INFOSTAT_INIT_COLUMNS,
        'melt_cols': MELT_COLS,
    }


class InfostatCleaningInfo:

    def __init__(self, file_type):
        self._file_type = file_type

    @property
    def _filter_df_by(self) -> List:
        return InfostatConfig.FILTER_DF_BY[self._file_type]

    @property
    def _rename_headers(self) -> Dict:
        return InfostatConfig.INFOSTAT_INIT_COLUMNS[self._file_type]

    @property
    def _melt_cols(self):
        return InfostatConfig.MELT_COLS[self._file_type]

    @property
    def _shared_params(self):
        return {key: value[self._file_type] for (key, value) in InfostatConfig.SHARED_CLEANING_PARAMS.items()}

    @property
    def cleaning_strategy(self):
        return InfostatConfig.INFOSTAT_CLEANING_STRATEGY[self._file_type]

    def cleaning_params(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        params = self._shared_params
        if kwargs:
            params.update(kwargs)

        return params
