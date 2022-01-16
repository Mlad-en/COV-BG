from abc import ABC, abstractmethod
from typing import List

import pandas as pd

from code_base.data_bindings.column_naming_consts import COLUMN_HEADING_CONSTS as COL_HEAD


class CalcYLLBase(ABC):

    @staticmethod
    def add_mean_yll(df):
        df[COL_HEAD.PYLL_MEAN] = df.apply(
            lambda x:
            x[COL_HEAD.LIFE_EXPECTANCY] * x[COL_HEAD.EXCESS_MORTALITY_BASE]
            if x[COL_HEAD.EXCESS_MORTALITY_BASE] > 0 else 0,
            axis=1).round(1)
        df[COL_HEAD.PYLL_FLUCTUATION] = df.apply(
            lambda x:
            x[COL_HEAD.LIFE_EXPECTANCY] * x[COL_HEAD.CONFIDENCE_INTERVAL]
            if x[COL_HEAD.PYLL_MEAN] > 0 else 0,
            axis=1).round(1)

        # Filter out negative and null PYLL
        df = df[df[COL_HEAD.PYLL_MEAN] > 0]

        return df

    @staticmethod
    def add_avg_yll(df):
        """

        :param df:
        :param mode:
        :return:
        """

        df[COL_HEAD.PYLL_AVG_MEAN] = df.apply(
            lambda x: x[COL_HEAD.PYLL_MEAN] / x[COL_HEAD.EXCESS_MORTALITY_BASE],
            axis=1).round(2)

        df[COL_HEAD.PYLL_AVG_FLUC] = df.apply(
            lambda x:
            abs(
                    (x[COL_HEAD.PYLL_MEAN] + x[COL_HEAD.PYLL_FLUCTUATION])
                    /
                    (x[COL_HEAD.EXCESS_MORTALITY_BASE] + x[COL_HEAD.CONFIDENCE_INTERVAL]) - x[COL_HEAD.PYLL_AVG_MEAN]
            ),
            axis=1).round(2)
        return df

    @staticmethod
    def add_std_mean_yll(df, mode: str = 'PYLL'):
        """

        :param df:
        :param mode:
        :return:
        """

        df[COL_HEAD.PYLL_STD_MEAN] = df.apply(
            lambda x:
            (x[f'{mode}_mean'] / x[COL_HEAD.POPULATION]) * (10 ** 5),
            axis=1).round(1)

        df[COL_HEAD.PYLL_STD_FLUC] = df.apply(
            lambda x:
            (x[f'{mode}_fluc'] / x[COL_HEAD.POPULATION]) * (10 ** 5),
            axis=1).round(1)

        return df

    @abstractmethod
    def calc_pyll(self, ages: List, sexes: List):
        pass


class CalcPYLL(CalcYLLBase):

    def __init__(self, es_mortality_df: pd.DataFrame, who_life_expectancy: pd.DataFrame, es_population: pd.DataFrame):
        self.es_population = es_population
        self.es_mortality_df = es_mortality_df
        self.who_life_expectancy = who_life_expectancy

    @property
    def mortality_to_life_expectancy(self):
        return [COL_HEAD.AGE, COL_HEAD.SEX, COL_HEAD.LOCATION]

    @property
    def mortality_to_population(self):
        return [COL_HEAD.SEX, COL_HEAD.LOCATION]

    def calc_pyll(self, ages: List, sexes: List):
        pyll = self.es_mortality_df.merge(self.who_life_expectancy, on=self.mortality_to_life_expectancy)
        pyll = self.add_mean_yll(pyll)

