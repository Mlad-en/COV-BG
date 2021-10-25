from typing import List

from code_base.data_cleaners.cleaning_params.infostat_params import InfostatHeaders, InfostatParams
from code_base.data_cleaners.cleaning_strategies.infostat_cleaning_strategies import *


class InfostatConfig:
    AVAILABLE_DATASETS = {
        'bg_pop_by_age_sex_reg',
        'avg_life_expectancy_by_sex',
        'life_expectancy_by_sex',
        'mortality_by_age_sex_mun',
        'population_by_municipality',
    }

    FILTER_DF_BY = {
        'bg_pop_by_age_sex_reg': [InfostatHeaders.FEMALE_EN, InfostatHeaders.MALE_EN],
        'avg_life_expectancy_by_sex': [InfostatHeaders.FEMALE_EN, InfostatHeaders.MALE_EN],
        'life_expectancy_by_sex': [InfostatHeaders.FEMALE_EN, InfostatHeaders.MALE_EN],
        'mortality_by_age_sex_mun': [InfostatHeaders.FEMALE_BG, InfostatHeaders.MALE_BG],
        'population_by_municipality': [InfostatHeaders.FEMALE_BG, InfostatHeaders.MALE_BG],
    }

    INFOSTAT_CLEANING_STRATEGY = {
        'bg_pop_by_age_sex_reg': PopulationAgeSexRegionCleaningStrategy,
        'avg_life_expectancy_by_sex': AVGLifeExpectancyBySexCleaningStrategy,
        'life_expectancy_by_sex': LifeExpectancyBySexCleaningStrategy,
        'mortality_by_age_sex_mun': MortalityByAgeSexMunicipalityCleaningStrategy,
        'population_by_municipality': PopulationByMunicipalityCleaningStrategy,
    }

    INFOSTAT_INIT_COLUMNS = {
        'bg_pop_by_age_sex_reg': InfostatParams().cols_pop_by_age_sex_reg,
        'avg_life_expectancy_by_sex': InfostatParams().cols_avg_life_expectancy_by_sex,
        'life_expectancy_by_sex': InfostatParams().cols_life_expectancy_by_sex,
        'mortality_by_age_sex_mun': InfostatParams().cols_mortality_by_age_sex_mun,
        'population_by_municipality': InfostatParams().cols_population_by_municipality,
    }

    MELT_COLS = {
        'bg_pop_by_age_sex_reg': {'id_vars': [InfostatHeaders.LOCATION, InfostatHeaders.AGE],
                                  'var_name': InfostatHeaders.SEX,
                                  'value_name': InfostatHeaders.POPULATION},

        'avg_life_expectancy_by_sex': {'id_vars': [InfostatHeaders.LOCATION],
                                       'var_name': InfostatHeaders.SEX,
                                       'value_name': InfostatHeaders.LIFE_EXPECTANCY},

        'life_expectancy_by_sex': {'id_vars': [InfostatHeaders.AGE],
                                   'var_name': InfostatHeaders.SEX,
                                   'value_name': InfostatHeaders.LIFE_EXPECTANCY},

        'mortality_by_age_sex_mun': {'id_vars': [InfostatHeaders.LOCATION],
                                     'var_name': InfostatHeaders.YEAR_SEX,
                                     'value_name': InfostatHeaders.MORTALITY},

        'population_by_municipality': {'id_vars': [InfostatHeaders.LOCATION],
                                       'var_name': InfostatHeaders.SEX,
                                       'value_name': InfostatHeaders.POPULATION},
    }


class InfostatCleaningInfo:

    def __init__(self, file_type):
        if file_type not in InfostatConfig.AVAILABLE_DATASETS:
            available_pages = ', '.join(InfostatConfig.AVAILABLE_DATASETS)
            raise ValueError(f'Incorrect infostat file type selected. Available file types: {available_pages}')

        self._file_type = file_type

    @property
    def filter_df_by(self) -> List:
        return InfostatConfig.FILTER_DF_BY[self._file_type]

    @property
    def rename_headers(self) -> Dict:
        return InfostatConfig.INFOSTAT_INIT_COLUMNS[self._file_type]

    @property
    def melt_cols(self):
        return InfostatConfig.MELT_COLS[self._file_type]

    @property
    def cleaning_strategy(self):
        return InfostatConfig.INFOSTAT_CLEANING_STRATEGY[self._file_type]
