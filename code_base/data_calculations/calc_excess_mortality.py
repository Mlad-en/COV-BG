from math import sqrt
from typing import List

import numpy as np
import pandas as pd

from code_base.data_bindings.column_naming_consts import COLUMN_HEADING_CONSTS as COL_HEAD


class CalculateEurostatExcessMortality:
    """

    """

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def _calc_std_dev(self, years: List):
        """

        :param years:
        :return:
        """
        self.df[COL_HEAD.STANDARD_DEVIATION] = self.df.loc[:, years].std(axis=1, ddof=0).round(1)

    def _add_zscore_con_int(self):
        """

        :return:
        """
        self.df[COL_HEAD.Z_SCORE] = 1.96
        self.df[COL_HEAD.CONFIDENCE_INTERVAL] = self.df.apply(
            lambda x: x[COL_HEAD.Z_SCORE] * (x[COL_HEAD.STANDARD_DEVIATION] / sqrt(5)),
            axis=1).round(1)

    def add_mean_mort(self, years: List):
        """

        :param years:
        :return:
        """
        self.df[COL_HEAD.MEAN_MORTALITY] = self.df[years].mean(axis=1).round(1)

    def _add_mean_mort_boundaries(self):
        """

        :return:
        """
        self.df[COL_HEAD.LB_MEAN_MORTALITY] = self.df[COL_HEAD.MEAN_MORTALITY] - self.df[COL_HEAD.CONFIDENCE_INTERVAL]
        self.df[COL_HEAD.UB_MEAN_MORTALITY] = self.df[COL_HEAD.MEAN_MORTALITY] + self.df[COL_HEAD.CONFIDENCE_INTERVAL]

    def _add_excess_mort(self, analyze_year):
        """

        :param analyze_year:
        :return:
        """
        self.df[COL_HEAD.EXCESS_MORTALITY_MEAN] = self.df.apply(
            lambda x: x[analyze_year] - x[COL_HEAD.MEAN_MORTALITY],
            axis=1).round(1)

    def _add_pscore(self, analyze_year):
        """

        :param analyze_year:
        :return:
        """
        self.df[COL_HEAD.P_SCORE] = self.df.apply(
            lambda x:
            (
                    (x[analyze_year] - x[COL_HEAD.MEAN_MORTALITY])
                    /
                    x[COL_HEAD.MEAN_MORTALITY]
            ) * 100
            if x[COL_HEAD.MEAN_MORTALITY] != 0
            else 0,
            axis=1).round(1)

        self.df[COL_HEAD.P_SCORE_FLUCTUATION] = self.df.apply(
            lambda x:
            x[COL_HEAD.P_SCORE]
            -
            (
                    (
                            (x[analyze_year] - x[COL_HEAD.UB_MEAN_MORTALITY])
                            / x[COL_HEAD.UB_MEAN_MORTALITY]
                    )
                    * 100
            )
            if x[COL_HEAD.UB_MEAN_MORTALITY] != 0
            else np.nan,
            axis=1).round(1)

    def _concat_column_vals(self, main_col, additional_col, brackets: List):
        return self.df[main_col].map(str) + brackets[0] + self.df[additional_col].map(str) + brackets[1]

    def _add_formatted_cols(self):
        self.df[COL_HEAD.MEAN_MORTALITY_DECORATED] = self._concat_column_vals(COL_HEAD.MEAN_MORTALITY,
                                                                              COL_HEAD.CONFIDENCE_INTERVAL,
                                                                              [' (±', ')'])
        self.df[COL_HEAD.EXCESS_MORTALITY_DECORATED] = self._concat_column_vals(COL_HEAD.EXCESS_MORTALITY_MEAN,
                                                                                COL_HEAD.CONFIDENCE_INTERVAL,
                                                                                [' (±', ')'])
        self.df[COL_HEAD.P_SCORE_DECORATED] = self._concat_column_vals(COL_HEAD.P_SCORE,
                                                                       COL_HEAD.P_SCORE_FLUCTUATION,
                                                                       ['% (±', '%)'])

    def _calculate_non_dec_excess_mortality(self, compare_years: List, analyze_year: str):
        self._calc_std_dev(compare_years)
        self._add_zscore_con_int()
        self._add_mean_mort_boundaries()
        self._add_excess_mort(analyze_year)
        self._add_pscore(analyze_year)

    def calculate_excess_mortality(self, compare_years: List, analyze_year: str):
        self._calculate_non_dec_excess_mortality(compare_years, analyze_year)
        self._add_formatted_cols()

        return self.df


class CalculateEurostatExcessMortalityToPopulation(CalculateEurostatExcessMortality):

    def __init__(self, df: pd.DataFrame, population_df: pd.DataFrame, merge_on: List):
        self.population_df = population_df
        self.merge_on = merge_on
        super().__init__(df)

    def _calc_pop_to_excess_mortality(self):
        """

        :return:
        """
        self.df = self.df.merge(self.population_df, on=self.merge_on)

        self.df[COL_HEAD.EXCESS_MORTALITY_PER_100_000] = self.df.apply(
            lambda x: x[COL_HEAD.EXCESS_MORTALITY_MEAN] / x[COL_HEAD.POPULATION] * 100_000,
            axis=1).round(1)

        self.df[COL_HEAD.EXCESS_MORTALITY_PER_100_000_FLUCTUATION] = self.df.apply(
            lambda x:
            abs(
                (
                        (x[COL_HEAD.EXCESS_MORTALITY_MEAN] + x[COL_HEAD.CONFIDENCE_INTERVAL])
                        / x[COL_HEAD.POPULATION] * 100_000
                )
                - x[COL_HEAD.EXCESS_MORTALITY_PER_100_000]
            ),
            axis=1).round(1)

    def _add_formatted_cols(self):
        super()._add_formatted_cols()
