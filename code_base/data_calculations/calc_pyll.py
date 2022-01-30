from typing import List

import pandas as pd

from code_base.data_calculations.utils import yll_source
from code_base.data_bindings.column_naming_consts import COLUMN_HEADING_CONSTS as COL_HEAD


class CalcPYLL:

    def __init__(self,
                 years: List[int],
                 ages: List[int],
                 sexes: List[str],
                 from_week: int,
                 static_over_90: bool):

        self.life_expectancy = yll_source.YLLLifeExpectancy(ages, static_over_90).get_life_expectancy()
        self.exc_mort = yll_source.YLLExcessMortality(years, ages, sexes, from_week).get_excess_mortality()
        self.full_pop = yll_source.YLLPopulation(years, ages, sexes).get_full_population()

    @staticmethod
    def _add_mean_yll(df):
        df[COL_HEAD.PYLL_MEAN] = df.apply(lambda x:
                                          x[COL_HEAD.LIFE_EXPECTANCY] * x[COL_HEAD.EXCESS_MORTALITY_MEAN]
                                          if x[COL_HEAD.EXCESS_MORTALITY_MEAN] > 0
                                          else 0,
                                          axis=1).round(1)

        df[COL_HEAD.PYLL_FLUCTUATION] = df.apply(lambda x:
                                                 x[COL_HEAD.LIFE_EXPECTANCY] * x[COL_HEAD.CONFIDENCE_INTERVAL]
                                                 if x[COL_HEAD.PYLL_MEAN] > 0
                                                 else 0,
                                                 axis=1).round(1)

        return df

    @staticmethod
    def _filter_non_significant_mortality(df):
        return df.loc[(df[COL_HEAD.IS_SIGNIFICANT] == 'Significant Increase'), :]

    @staticmethod
    def _agg_exc_mort_yll(df):
        agg_params = {COL_HEAD.EXCESS_MORTALITY_MEAN: 'sum',
                      COL_HEAD.CONFIDENCE_INTERVAL:   'sum',
                      COL_HEAD.PYLL_MEAN:             'sum',
                      COL_HEAD.PYLL_FLUCTUATION:      'sum',
                      }
        return df.groupby([COL_HEAD.SEX, COL_HEAD.LOCATION, COL_HEAD.IS_SIGNIFICANT], as_index=False).agg(agg_params)

    @staticmethod
    def _add_avg_yll(df):
        df[COL_HEAD.PYLL_AVG_MEAN] = df.apply(lambda x:
                                              x[COL_HEAD.PYLL_MEAN] / x[COL_HEAD.EXCESS_MORTALITY_MEAN],
                                              axis=1).round(2)

        df[COL_HEAD.PYLL_AVG_FLUC] = df.apply(lambda x:
                                              abs(
                                                  (x[COL_HEAD.PYLL_MEAN] + x[COL_HEAD.PYLL_FLUCTUATION])
                                                  /
                                                  (x[COL_HEAD.EXCESS_MORTALITY_MEAN] + x[COL_HEAD.CONFIDENCE_INTERVAL])
                                                  - x[COL_HEAD.PYLL_AVG_MEAN]
                                              ),
                                              axis=1).round(2)

        return df

    @staticmethod
    def _group_pop(df):
        return df.groupby([COL_HEAD.SEX, COL_HEAD.LOCATION], as_index=False)[COL_HEAD.POPULATION].sum()

    @staticmethod
    def _add_std_mean_yll(df):
        df[COL_HEAD.PYLL_STD_MEAN] = df.apply(lambda x:
                                              (x[COL_HEAD.PYLL_MEAN] / x[COL_HEAD.POPULATION])
                                              *
                                              10 ** 5,
                                              axis=1).round(1)

        df[COL_HEAD.PYLL_STD_FLUC] = df.apply(lambda x:
                                              (x[COL_HEAD.PYLL_FLUCTUATION] / x[COL_HEAD.POPULATION])
                                              *
                                              10 ** 5,
                                              axis=1).round(3)

        return df

    @staticmethod
    def _merge_mean_fluc_cols(df):
        df[COL_HEAD.PYLL_MEAN_DECORATED] = df[COL_HEAD.PYLL_MEAN].round(1).map(str) + ' (±' + df[
            COL_HEAD.PYLL_FLUCTUATION].round(1).map(str) + ')'
        df[COL_HEAD.PYLL_AVG_MEAN_DECORATED] = df[COL_HEAD.PYLL_AVG_MEAN].map(str) + ' (±' + df[
            COL_HEAD.PYLL_AVG_FLUC].map(str) + ')'
        df[COL_HEAD.PYLL_STD_MEAN_DECORATED] = df[COL_HEAD.PYLL_STD_MEAN].map(str) + ' (±' + df[
            COL_HEAD.PYLL_STD_FLUC].map(str) + ')'

        return df

    def calculate(self) -> pd.DataFrame:
        full_pop = self._group_pop(self.full_pop)
        exc_mort = self.exc_mort.merge(self.life_expectancy, on=[COL_HEAD.AGE, COL_HEAD.SEX, COL_HEAD.LOCATION])
        exc_mort = self._add_mean_yll(exc_mort)
        exc_mort = self._filter_non_significant_mortality(exc_mort)
        exc_mort = self._agg_exc_mort_yll(exc_mort)
        exc_mort = self._add_avg_yll(exc_mort)

        exc_mort = exc_mort.merge(full_pop, on=[COL_HEAD.SEX, COL_HEAD.LOCATION])
        exc_mort = self._add_std_mean_yll(exc_mort)
        exc_mort = self._merge_mean_fluc_cols(exc_mort)

        return exc_mort.sort_values([COL_HEAD.PYLL_STD_MEAN, COL_HEAD.SEX], ascending=False)

