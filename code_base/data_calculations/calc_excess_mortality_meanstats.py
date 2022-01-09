from math import sqrt
from typing import List

import numpy as np
import pandas as pd

from code_base.data_bindings.column_naming_consts import COLUMN_HEADING_CONSTS as COL_HEAD


class CalculateEurostatExcessMortalityMean:
    """

    """

    @staticmethod
    def _calc_std_dev(df: pd.DataFrame, years: List):
        """

        :param df:
        :param years:
        :return:
        """
        df[COL_HEAD.STANDARD_DEVIATION] = df.loc[:, years].std(axis=1, ddof=0).round(1)

        return df

    @staticmethod
    def _add_zscore_con_int(df: pd.DataFrame):
        """

        :param df:
        :return:
        """
        df[COL_HEAD.Z_SCORE] = 1.96
        df[COL_HEAD.CONFIDENCE_INTERVAL] = df.apply(
            lambda x: x[COL_HEAD.Z_SCORE] * (x[COL_HEAD.STANDARD_DEVIATION] / sqrt(5)),
            axis=1).round(1)

        return df

    @staticmethod
    def add_mean_mort(df: pd.DataFrame, years: List):
        """

        :param df:
        :param years:
        :return:
        """
        df[COL_HEAD.MEAN_OR_EXPECTED_MORTALITY] = df[years].mean(axis=1).round(1)

        return df

    @staticmethod
    def _add_mean_mort_boundaries(df: pd.DataFrame):
        """

        :return:
        """
        df[COL_HEAD.LB_MEAN_MORTALITY] = df[COL_HEAD.MEAN_OR_EXPECTED_MORTALITY] - df[COL_HEAD.CONFIDENCE_INTERVAL]
        df[COL_HEAD.UB_MEAN_MORTALITY] = df[COL_HEAD.MEAN_OR_EXPECTED_MORTALITY] + df[COL_HEAD.CONFIDENCE_INTERVAL]

        return df

    @staticmethod
    def _add_excess_mort(df: pd.DataFrame, analyze_year):
        """

        :param analyze_year:
        :return:
        """
        df[COL_HEAD.EXCESS_MORTALITY_MEAN] = df.apply(
            lambda x: x[analyze_year] - x[COL_HEAD.MEAN_OR_EXPECTED_MORTALITY],
            axis=1).round(1)

        return df

    @staticmethod
    def _add_pscore(df: pd.DataFrame, analyze_year):
        """

        :param df:
        :param analyze_year:
        :return:
        """
        df[COL_HEAD.P_SCORE] = df.apply(
            lambda x:
            (
                    (x[analyze_year] - x[COL_HEAD.MEAN_OR_EXPECTED_MORTALITY])
                    /
                    x[COL_HEAD.MEAN_OR_EXPECTED_MORTALITY]
            ) * 100
            if x[COL_HEAD.MEAN_OR_EXPECTED_MORTALITY] != 0
            else 0,
            axis=1).round(1)

        df[COL_HEAD.P_SCORE_FLUCTUATION] = df.apply(
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

        return df

    @staticmethod
    def _concat_column_vals(df: pd.DataFrame, main_col, additional_col, brackets: List):
        return df[main_col].map(str) + brackets[0] + df[additional_col].map(str) + brackets[1]

    def _add_formatted_cols(self, df: pd.DataFrame):
        df[COL_HEAD.MEAN_MORTALITY_DECORATED] = self._concat_column_vals(df,
                                                                         COL_HEAD.MEAN_OR_EXPECTED_MORTALITY,
                                                                         COL_HEAD.CONFIDENCE_INTERVAL,
                                                                         [' (±', ')'])

        df[COL_HEAD.EXCESS_MORTALITY_DECORATED] = self._concat_column_vals(df,
                                                                           COL_HEAD.EXCESS_MORTALITY_MEAN,
                                                                           COL_HEAD.CONFIDENCE_INTERVAL,
                                                                           [' (±', ')'])

        df[COL_HEAD.P_SCORE_DECORATED] = self._concat_column_vals(df,
                                                                  COL_HEAD.P_SCORE,
                                                                  COL_HEAD.P_SCORE_FLUCTUATION,
                                                                  ['% (±', '%)'])

        return df

    def _calculations_with_mean_mortality(self, df: pd.DataFrame, compare_years: List, analyze_year: int):
        df = self._calc_std_dev(df, compare_years)
        df = self._add_zscore_con_int(df)
        df = self._add_mean_mort_boundaries(df)
        df = self._add_excess_mort(df, analyze_year)
        df = self._add_pscore(df, analyze_year)

        return df

    def calculate_excess_mortality(self, df: pd.DataFrame, compare_years: List, analyze_year: int):

        df = self._calculations_with_mean_mortality(df, compare_years, analyze_year)
        df = self._add_formatted_cols(df)

        return df