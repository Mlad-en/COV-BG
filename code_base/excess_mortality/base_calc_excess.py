from typing import List, Union

import pandas as pd
from math import sqrt
import numpy as np


class ExcessMortBase:
    def __init__(self, analyze_year: Union[str, int]):
        self.anlz_yr = str(analyze_year)

    # noinspection PyTypeChecker
    @staticmethod
    def add_zscore_con_int(df: pd.DataFrame) -> pd.DataFrame:
        df['Z-Score(95%)'] = 1.96
        df['Conf_interval'] = df.apply(lambda x: x['Z-Score(95%)']
                                                 *
                                                 (x['STD'] / sqrt(5)),
                                       axis=1).round(1)

        return df

    @staticmethod
    def calc_std_dev(df: pd.DataFrame, years: List) -> pd.DataFrame:
        df['STD'] = df.loc[:, years].std(axis=1, ddof=0).round(1)
        return df

    @staticmethod
    def add_mean_mort(df: pd.DataFrame, years: List) -> pd.DataFrame:
        df['Mean_Mortality'] = df[years].mean(axis=1).round(1)

        return df

    @staticmethod
    def add_mean_mort_boundaries(df: pd.DataFrame) -> pd.DataFrame:
        df['Lower_bound_Mean_mortality'] = df['Mean_Mortality'] - df['Conf_interval'].round(1)
        df['Upper_bound_Mean_mortality'] = df['Mean_Mortality'] + df['Conf_interval'].round(1)

        return df

    # noinspection PyTypeChecker
    def add_excess_mort(self, df: pd.DataFrame) -> pd.DataFrame:
        df['Excess_mortality_Mean'] = df.apply(lambda x: x[self.anlz_yr] - x['Mean_Mortality'], axis=1).round(1)
        df['Excess_mortality_fluc'] = df.apply(lambda x:
                                               abs(
                                                   x['Excess_mortality_Mean'] -
                                                   (x[self.anlz_yr] - x['Lower_bound_Mean_mortality'])
                                               ),
                                               axis=1).round(1)
        return df

    def add_pscore(self, df: pd.DataFrame) -> pd.DataFrame:
        df['P_Score'] = df.apply(lambda x:
                                 (
                                         (x[self.anlz_yr] - x['Mean_Mortality'])
                                         /
                                         x['Mean_Mortality']
                                 ) * 100
                                 if x['Mean_Mortality'] != 0
                                 else 0,
                                 axis=1).round(1)

        df['P_score_fluctuation'] = df.apply(lambda x:
                                             (x['P_Score']
                                              -
                                              (
                                                      (
                                                              (x[self.anlz_yr] - x['Upper_bound_Mean_mortality'])
                                                              /
                                                              x['Upper_bound_Mean_mortality']
                                                      )
                                                      * 100
                                              )
                                              )
                                             if x['Upper_bound_Mean_mortality'] != 0
                                             else np.nan,
                                             axis=1).round(1)
        return df

    @staticmethod
    def add_formatted_attrs(df) -> pd.DataFrame:
        df['Mean Mortality ±'] = df['Mean_Mortality'].round(1).map(str) + ' (±' + df['Conf_interval'].map(str) + ')'
        df['Excess Mortality ±'] = df['Excess_mortality_Mean'].map(str) + ' (±' + df['Excess_mortality_fluc'].map(
            str) + ')'
        df['P_score ±'] = df['P_Score'].map(str) + '% (±' + df['P_score_fluctuation'].map(str) + '%)'
        return df

    @staticmethod
    def calc_pop_to_excess_mortality(mortality_df, pop_df, merge_on):
        """

        :param mortality_df:
        :param pop_df:
        :param merge_on:
        :return:
        """
        exc_mort_std = mortality_df.merge(pop_df,
                                          on=merge_on).copy()

        exc_mort_std['Excess_mortality_per_10^5'] = exc_mort_std.apply(
            lambda x: x['Excess_mortality_Mean'] / x['Population'] * 10 ** 5, axis=1).round(1)

        exc_mort_std['Excess_mortality_per_10^5_fluc'] = exc_mort_std.apply(
            lambda x: abs(((x['Excess_mortality_Mean'] + x['Excess_mortality_fluc']) / x['Population'] * 10 ** 5) - x[
                'Excess_mortality_per_10^5']), axis=1).round(1)

        exc_mort_std['Excess_mortality_per_10^5_±'] = \
            exc_mort_std['Excess_mortality_per_10^5'].map(str) \
            + '(±' + \
            exc_mort_std['Excess_mortality_per_10^5_fluc'].map(str) \
            + ')'

        return exc_mort_std

    def add_exc_mort_info(self, df: pd.DataFrame, prev_years: List, add_mean_mort: bool = True) -> pd.DataFrame:
        """

        :param df:
        :param prev_years:
        :param add_mean_mort:
        :return:
        """
        if add_mean_mort:
            df = self.add_mean_mort(df, prev_years)
        df = self.calc_std_dev(df, prev_years)
        df = self.add_zscore_con_int(df)
        df = self.add_mean_mort_boundaries(df)
        df = self.add_excess_mort(df)
        df = self.add_pscore(df)
        df = self.add_formatted_attrs(df)

        return df
