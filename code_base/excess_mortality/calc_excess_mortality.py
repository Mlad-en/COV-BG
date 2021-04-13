from math import sqrt
from typing import Optional, List, Dict

import numpy as np
import pandas as pd

from code_base.excess_mortality.folder_constants import *
from code_base.excess_mortality.get_excess_mortality import ExcessMortalityMapper
from code_base.utils.file_utils import SaveFile


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
                                  week_end: int = 53,
                                  add_age: bool = False) -> pd.DataFrame:
        """
        :param df: Provide a Dataframe object containing weekly mortality.
        :param week_start: Defines the starting week of the previous year comparison. Default = 10
        :param week_end: Defines the ending week of the previous year comparison. Default = 53
        :param add_age:
        :return: Returns a pivoted version of the provided Dataframe, filtered by year (2015-2019) and weeks.
        The returned Dataframe includes Mean Mortality.
        """
        pivoted = df[(df['Year'] < 2020) & (df['Week'] >= week_start) & (df['Week'] <= week_end)].copy()

        if not add_age:
            pivoted.drop('Age', axis=1, inplace=True)
            pivoted = pivoted.groupby(['Sex', 'Location', 'Year', 'Week'], as_index=False).sum('Mortality')
            pivoted = pivoted.pivot(index=['Sex', 'Location', 'Week'], columns='Year', values='Mortality').reset_index()
        else:
            pivoted = pivoted.groupby(['Age', 'Sex', 'Location', 'Year', 'Week'], as_index=False).sum('Mortality')
            pivoted = pivoted.pivot(index=['Age', 'Sex', 'Location', 'Week'], columns='Year', values='Mortality').reset_index()

        pivoted['Mean_Mortality'] = pivoted[[2015, 2016, 2017, 2018, 2019]].mean(axis=1).round(1)

        return pivoted

    @staticmethod
    def setup_weekly_std(df: pd.DataFrame) -> pd.DataFrame:
        """For all years which have only 52 weeks, copy mortality for week 52 to week 53.
        This is similar to the way it is handled in https://ourworldindata.org/excess-mortality-covid,
        where they all together compare data from week 52 for all previous years (Endnote #5)."""
        df.fillna(method='pad', inplace=True)
        return df

    @staticmethod
    def setup_yearly_std(df: pd.DataFrame, add_age: bool = False) -> pd.DataFrame:
        # Remove Weekly column and aggregate weekly mortality.
        group_params = {
            True: ['Age', 'Sex', 'Location'],
            False: ['Sex', 'Location'],
        }
        df.drop('Week', axis=1, inplace=True)
        df = df.groupby(group_params[add_age], as_index=False).sum('Mortality')
        return df

    def add_std(self, df, setup_param: str = 'year', add_age: bool = False) -> pd.DataFrame:
        setup = {
            'year': self.setup_yearly_std,
            'week': self.setup_weekly_std
        }
        if add_age and setup_param == 'year':
            df = setup[setup_param](df, add_age)
        else:
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
                                  week_end: int = 53,
                                  add_age: bool = False
                                  ) -> pd.DataFrame:
        curr_year_mort = df[(df['Year'] >= 2020) &
                            (
                                    (df['Year'] == 2020) & (df['Week'] >= week_start) & (df['Week'] <= week_end)
                            )]
        if not add_age:
            curr_year_mort.drop('Age', axis=1, inplace=True)
            curr_year_mort = curr_year_mort.groupby(['Sex', 'Location', 'Year', 'Week'], as_index=False).sum('Mortality')
        else:
            curr_year_mort = curr_year_mort.groupby(['Age', 'Sex', 'Location', 'Year', 'Week'], as_index=False).sum('Mortality')
        return curr_year_mort

    @staticmethod
    def merge_weekly_dfs(curr_year: pd.DataFrame, prev_years: pd.DataFrame, param: str = 'year', add_age: bool = False) -> pd.DataFrame:
        if not add_age:
            merge_data_on = {
                'year': ['Sex', 'Location'],
                'week': ['Sex', 'Location', 'Week']
            }
        else:
            merge_data_on = {
                'year': ['Age', 'Sex', 'Location'],
                'week': ['Age', 'Sex', 'Location', 'Week']
            }

        if param == 'year':
            curr_year.drop('Week', axis=1, inplace=True)
            if not add_age:
                curr_year = curr_year.groupby(['Sex', 'Location', 'Year'], as_index=False).sum('Mortality')
            else:
                curr_year = curr_year.groupby(['Age', 'Sex', 'Location', 'Year'], as_index=False).sum('Mortality')

        curr_year = curr_year.merge(prev_years,
                                    left_on=merge_data_on[param],
                                    right_on=merge_data_on[param])
        return curr_year

    @staticmethod
    def add_merged_data_attrs(df: pd.DataFrame) -> pd.DataFrame:
        df['Excess_mortality_Mean'] = df.apply(lambda x: x['Mortality'] - x['Mean_Mortality'], axis=1).round(1)
        df['Excess_mortality_fluc'] = df.apply(lambda x:
                                             abs(x['Excess_mortality_Mean'] - (x['Mortality'] - x['Lower_bound_Mean_mortality'])),
                                             axis=1).round(1)
        df['P_Score'] = df.apply(
                lambda x: ((x['Mortality'] - x['Mean_Mortality']) / x['Mean_Mortality']) * 100
                if x['Mean_Mortality']!=0 else 0,
                axis=1).round(1)
        df['P_score_fluctuation'] = df.apply(
                lambda x: (x['P_Score'] - (
                            ((x['Mortality'] - x['Upper_bound_Mean_mortality']) / x['Upper_bound_Mean_mortality']) * 100))
            if x['Upper_bound_Mean_mortality'] !=0
                else np.nan,
                axis=1).round(1)

        df['Mean Mortality ±'] = df['Mean_Mortality'].round(1).map(str) + ' (±' + df['Conf_interval'].map(str) + ')'
        df['Excess Mortality ±'] = df['Excess_mortality_Mean'].map(str) + ' (±' + df['Excess_mortality_fluc'].map(
            str) + ')'
        df['P_score ±'] = df['P_Score'].map(str) + '% (±' + df['P_score_fluctuation'].map(str) + '%)'
        return df

    @staticmethod
    def calc_std_pop_excess_mortality(mortality_df, pop_df):
        exc_mort_std: pd.DataFrame = mortality_df.merge(pop_df[['Sex', 'Location', 'Population']],
                                                        left_on=['Sex', 'Location'],
                                                        right_on=['Sex', 'Location']).copy()

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

    def calc_excess_mortality(self,
                              df: pd.DataFrame,
                              weekly: bool = False,
                              add_age: bool = False) -> pd.DataFrame:
        time_params = {
            False: 'year',
            True: 'week'
        }
        time_param = time_params[weekly]

        prev_years = self.build_prev_year_mort_base(df, add_age=add_age)
        prev_years = self.add_std(prev_years, time_param, add_age=add_age)
        prev_years = self.add_cmn_prev_year_attrs(prev_years)

        curr_year = self.build_curr_year_mort_base(df=df, add_age=add_age)
        merged: pd.DataFrame = self.merge_weekly_dfs(curr_year=curr_year,
                                                     prev_years=prev_years,
                                                     param=time_param,
                                                     add_age=add_age)
        merged: pd.DataFrame = self.add_merged_data_attrs(merged)

        return merged

    def clean_eu_data(self, df, exclude_cntrs: Optional[List] = ['']):
        year = 2021 if self.add_current_year else 2020
        week = self.current_year_weeks if self.add_current_year else 53

        filt_mask = ((df['Year'] == year)
                     & (df['Week'] == week)
                     & (df['Mortality'].notnull())
                     & ~(df['Location'].isin(exclude_cntrs)))
        countries_w_uptodate_data = df[filt_mask].loc[:, 'Location'].drop_duplicates().to_list()

        df = df[df['Location'].isin(countries_w_uptodate_data)]

        return df

    def excess_mortality_to_file(self,
                                 mortality_df: pd.DataFrame,
                                 pop_df: pd.DataFrame,
                                 sex: List = ['Total'],
                                 age: List = ['Total'],
                                 exclude_cntrs: Optional[List] = ['']) -> Dict:
        """
        :param mortality_df: Add reference to the get_mortality_df attribute.
        :param pop_df:
        :param age: Specifies the list of age ranges included in the report (e.g. ['(10-14)', '(15-19)', '(20-24)', 'Total'])
        :param sex: Specifies the list of sexes included in the report (e.g. [Male, Female, Total]).
        :param exclude_cntrs: a List of countries that require an exclusion from the Dataset.
        :return: Function returns a dictionary of the file location of the per week deaths (key: weekly_deaths)
        and total deaths (key: total_deaths)
        """
        df = mortality_df
        df = df[(df['Age'].isin(age)) & (df['Sex'].isin(sex))]

        if not self.cntry:
            df = self.clean_eu_data(df, exclude_cntrs=exclude_cntrs)

        country = f'{self.cntry}_' if self.cntry else 'EUROPE_'
        age_f = self.get_age_ranges(age)

        total_file_name = f'TOTAL_{country}{age_f}_{sex}_excess_mortality_{self.get_year_ranges}'
        total_deaths = self.calc_excess_mortality(df)
        total_deaths_std = self.calc_std_pop_excess_mortality(total_deaths, pop_df)
        # total_deaths_std = total_deaths
        total_deaths_file = self.save_df_to_file(total_deaths_std, self.file_loc, total_file_name, method='excel')

        weekly_file_name = f'WEEKLY_{country}{age_f}_{sex}_excess_mortality_{self.get_year_ranges}'
        weekly_deaths = self.calc_excess_mortality(df, weekly=True)
        weekly_deaths_std = self.calc_std_pop_excess_mortality(weekly_deaths, pop_df)
        # weekly_deaths_std = weekly_deaths
        weekly_deaths_file = self.save_df_to_file(weekly_deaths_std, self.file_loc, weekly_file_name, method='excel')

        file_locs = {
            'total': total_deaths_file,
            'weekly': weekly_deaths_file
        }

        return file_locs