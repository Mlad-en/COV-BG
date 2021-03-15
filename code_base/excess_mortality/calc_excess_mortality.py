from math import sqrt
from os import path
from typing import Optional, List, Dict

import pandas as pd

from code_base.excess_mortality.folder_constants import *
from code_base.excess_mortality.get_excess_mortality import ExcessMortalityMapper
from code_base.excess_mortality.utils import SaveFile

class CalcExcessMortality(SaveFile):

    def __init__(self,
                 cntry: str = None,
                 add_current_year: bool = False,
                 current_year_weeks: Optional[int] = None):
        self.cntry = cntry
        self.add_current_year = add_current_year
        self.current_year_weeks = current_year_weeks

        self.file_loc = output_excess_mortality_regions if self.cntry else output_excess_mortality_countries

    @property
    def fetch_data(self) -> str:
        data = ExcessMortalityMapper(cntry=self.cntry,
                                     add_current_year=self.add_current_year,
                                     current_year_weeks=self.current_year_weeks)
        loc = data.generate_data()
        return loc

    @property
    def get_mortality_df(self) -> pd.DataFrame:
        file = self.fetch_data
        source_df = pd.read_csv(file)
        return source_df

    @property
    def get_year_ranges(self) -> str:
        if self.add_current_year:
            return f'2020_2021'
        else:
            return f'2020'

    @staticmethod
    def get_age_ranges(age_lst: List) -> str:
        if len(age_lst) > 1:
            return f'{age_lst[0]} - {age_lst[-1]}'
        else:
            return f'{age_lst[0]}'

    @staticmethod
    def build_prev_year_mort_base(df: pd.DataFrame,
                                  week_start: int = 10,
                                  week_end: int = 53) -> pd.DataFrame:
        """
        :param df: Provide a Dataframe object containing weekly mortality.
        :param week_start: Defines the starting week of the previous year comparison. Default = 10
        :param week_end: Defines the ending week of the previous year comparison. Default = 53
        :return: Returns a pivoted version of the provided Dataframe, filtered by year (2015-2019) and weeks.
        The returned Dataframe includes Mean Mortality.
        """
        pivoted = df[(df['Year'] < 2020) & (df['Week'] >= week_start) & (df['Week'] <= week_end)].copy()
        pivoted.drop('Age', axis=1, inplace=True)
        pivoted = pivoted.groupby(['Sex', 'Location', 'Year', 'Week'], as_index=False).sum('Mortality')
        pivoted = pivoted.pivot(index=['Sex', 'Location', 'Week'], columns='Year', values='Mortality').reset_index()
        pivoted['Mean_Mortality'] = pivoted[[2015, 2016, 2017, 2018, 2019]].mean(axis=1).round(1)

        return pivoted

    @staticmethod
    def setup_weekly_std(df: pd.DataFrame) -> pd.DataFrame:
        """For all years which have only 52 weeks, copy mortality for week 52 to week 53."""
        df.fillna(method='pad', inplace=True)
        return df

    @staticmethod
    def setup_yearly_std(df: pd.DataFrame) -> pd.DataFrame:
        # Remove Weekly column and aggregate weekly mortality.
        df.drop('Week', axis=1, inplace=True)
        df = df.groupby(['Sex', 'Location'], as_index=False).sum('Mortality')
        return df

    def add_std(self, df, setup_param: str = 'year') -> pd.DataFrame:
        setup = {
            'year': self.setup_yearly_std,
            'week': self.setup_weekly_std
        }
        df = setup[setup_param](df)
        df['STD'] = df.loc[:, [2015, 2016, 2017, 2018, 2019]].std(axis=1, ddof=0).round(1)

        return df

    @staticmethod
    def add_cmn_prev_year_attrs(df: pd.DataFrame) -> pd.DataFrame:
        df['Z-Score(95%)'] = 1.96
        df['Conf_interval'] = df.apply(lambda x: x['Z-Score(95%)'] * (x['STD'] / sqrt(5)), axis=1).round(1)
        df['Lower_bound_Mean_mortality'] = df['Mean_Mortality'] - df['Conf_interval'].round(1)
        df['Upper_bound_Mean_mortality'] = df['Mean_Mortality'] + df['Conf_interval'].round(1)

        return df

    @staticmethod
    def build_curr_year_mort_base(df: pd.DataFrame,
                                  week_start: int = 10,
                                  week_end: int = 53
                                  ) -> pd.DataFrame:
        curr_year_mort = df[(df['Year'] >= 2020) &
                            (
                                    (df['Year'] == 2020) & (df['Week'] >= week_start) & (df['Week'] <= week_end)
                            )]
        return curr_year_mort

    @staticmethod
    def merge_weekly_dfs(curr_year: pd.DataFrame, prev_years: pd.DataFrame, param: str = 'year') -> pd.DataFrame:
        merge_data_on = {
            'year': ['Sex', 'Location'],
            'week': ['Sex', 'Location', 'Week']
        }

        if param == 'year':
            curr_year.drop('Week', axis=1, inplace=True)
            curr_year = curr_year.groupby(['Age', 'Sex', 'Location', 'Year'], as_index=False).sum('Mortality')

        curr_year = curr_year.merge(prev_years,
                                    left_on=merge_data_on[param],
                                    right_on=merge_data_on[param])
        return curr_year

    @staticmethod
    def add_merged_data_attrs(df: pd.DataFrame) -> pd.DataFrame:
        df['Excess_mortality_Mean'] = df.apply(lambda x: x['Mortality'] - x['Mean_Mortality'], axis=1).round(1)
        df['Excess_mortality_fluc'] = df.apply(lambda x:
                                             x['Excess_mortality_Mean'] - (x['Mortality'] - x['Upper_bound_Mean_mortality']),
                                             axis=1).round(1)
        df['P_Score'] = df.apply(
            lambda x: ((x['Mortality'] - x['Mean_Mortality']) / x['Mean_Mortality']) * 100,
            axis=1).round(1)
        df['P_score_fluctuation'] = df.apply(
            lambda x: (x['P_Score'] - (
                        ((x['Mortality'] - x['Upper_bound_Mean_mortality']) / x['Upper_bound_Mean_mortality']) * 100)),
            axis=1).round(1)
        df['Mean Mortality ±'] = df['Mean_Mortality'].round(1).map(str) + ' (±' + df['Conf_interval'].map(str) + ')'
        df['Excess Mortality ±'] = df['Excess_mortality_Mean'].map(str) + ' (±' + df['Excess_mortality_fluc'].map(
            str) + ')'
        df['P_score ±'] = df['P_Score'].map(str) + '% (±' + df['P_score_fluctuation'].map(str) + '%)'

        return df

    def calc_excess_mortality(self,
                              df: pd.DataFrame,
                              age: List = ['Total'],
                              sex: List = ['Total'],
                              weekly: bool = False) -> pd.DataFrame:
        time_params = {
            False: 'year',
            True: 'week'
        }
        time_param = time_params[weekly]

        df = df[(df['Age'].isin(age)) & (df['Sex'].isin(sex))]
        prev_years = self.build_prev_year_mort_base(df)
        prev_years = self.add_std(prev_years, time_param)
        prev_years = self.add_cmn_prev_year_attrs(prev_years)

        curr_year = self.build_curr_year_mort_base(df=df)
        merged = self.merge_weekly_dfs(curr_year=curr_year, prev_years=prev_years,  param=time_param)
        merged = self.add_merged_data_attrs(merged)

        return merged

    def excess_mortality_to_file(self, mortality_df: pd.DataFrame, sex: List = ['Total'], age: List = ['Total']) -> Dict:
        # TODO: Add filtering for Countries that do not have data for all weeks required for analysis.
        # TODO: Add filtering for week start and end ranges.
        """
        :param mortality_df: Add reference to the get_mortality_df attribute.
        :param age: Specifies the list of age ranges included in the report (e.g. ['(10-14)', '(15-19)', '(20-24)', 'Total'])
        :param sex: Specifies the list of sexes included in the report (e.g. [Male, Female, Total]).
        :return: Function returns a dictionary of the file location of the per week deaths (key: weekly_deaths)
        and total deaths (key: total_deaths)
        """

        country = f'{self.cntry}_' if self.cntry else ''
        age_f = self.get_age_ranges(age)
        weekly_file_name = f'WEEKLY_{country}{age_f}_{sex}_excess_mortality_{self.get_year_ranges}'
        total_file_name = f'TOTAL_{country}{age_f}_{sex}_excess_mortality_{self.get_year_ranges}'

        df = mortality_df
        df = df[(df['Age'].isin(age)) & (df['Sex'].isin(sex))]

        total_deaths = self.calc_excess_mortality(df)
        total_file = self.save_df(total_deaths, self.file_loc, total_file_name)

        weekly_deaths = self.calc_excess_mortality(df, weekly=True)
        weekly_file = self.save_df(weekly_deaths, self.file_loc, weekly_file_name)

        file_locs = {
            'total_deaths': total_file,
            'weekly_deaths': weekly_file
        }
        return file_locs