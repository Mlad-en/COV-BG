from typing import List

import pandas as pd
from math import sqrt
import numpy as np


class ExcessMortBase:
    def __init__(self):
        pass

    @staticmethod
    def pad_data(df: pd.DataFrame) -> pd.DataFrame:
        df.fillna(method='pad', inplace=True)
        return df

    # noinspection PyTypeChecker
    @staticmethod
    def add_zscore_con_int(df: pd.DataFrame) -> pd.DataFrame:
        df['Z-Score(95%)'] = 1.96
        df['Conf_interval'] = df.apply(lambda x: x['Z-Score(95%)']
                                                 *
                                                 (x['STD'] / sqrt(5)), axis=1).round(1)

        return df

    @staticmethod
    def calc_std_dev(df, years: List):
        df['STD'] = df.loc[:, years].std(axis=1, ddof=0).round(1)
        return df

    @staticmethod
    def add_mean_mort(df, years: List):
        df['Mean_Mortality'] = df[years].mean(axis=1).round(1)
        df['Lower_bound_Mean_mortality'] = df['Mean_Mortality'] - df['Conf_interval'].round(1)
        df['Upper_bound_Mean_mortality'] = df['Mean_Mortality'] + df['Conf_interval'].round(1)

        return df

    # noinspection PyTypeChecker
    @staticmethod
    def add_excess_mort(df: pd.DataFrame) -> pd.DataFrame:
        df['Excess_mortality_Mean'] = df.apply(lambda x: x['2020'] - x['Mean_Mortality'], axis=1).round(1)
        df['Excess_mortality_fluc'] = df.apply(lambda x:
                                               abs(
                                                   x['Excess_mortality_Mean'] -
                                                   (x['2020'] - x['Lower_bound_Mean_mortality'])
                                               ),
                                               axis=1).round(1)
        return df

    @staticmethod
    def add_pscore(df):
        df['P_Score'] = df.apply(lambda x:
                                 (
                                         (x['2020'] - x['Mean_Mortality'])
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
                                                              (x['2020'] - x['Upper_bound_Mean_mortality'])
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