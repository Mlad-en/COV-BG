from os import path
from typing import List, Optional

import pandas as pd

from code_base.excess_mortality.calc_excess_mortality import CalcExcessMortality
from code_base.excess_mortality.decode_args import std_eu_pop_2013_decode_age
from code_base.pyll.url_constants import FED_INFO_SYS
from code_base.pyll.folder_constants import output_pyll_eu, source_std_eu_2013_pop_data
from code_base.pyll.get_life_data import GetWHOLifeData
from code_base.utils.common_query_params import exclude_cntrs, sex, ages_0_89, age_15_64, age_85_89, ages_0_84
from code_base.excess_mortality.get_population_eu import GetPopUN, GetEUPopulation

from code_base.utils.save_file_utils import SaveFile


class CalcExcessMortYLL(SaveFile):
    def __init__(self):
        self.file_location = output_pyll_eu

    @property
    def get_excess_mortality(self) -> pd.DataFrame:
        eu_mortality = CalcExcessMortality()
        mortality = eu_mortality.get_mortality_df
        exc_mort = eu_mortality.calc_excess_mortality(eu_mortality.clean_eu_data(mortality, exclude_cntrs),
                                                      add_age=True)

        relevant_cols = ['Age', 'Sex', 'Location', 'Excess_mortality_Mean', 'Excess_mortality_fluc']
        exc_mort.drop(columns=[col for col in exc_mort if col not in relevant_cols], inplace=True)

        return exc_mort

    @property
    def get_life_exp_eu(self) -> pd.DataFrame:
        eu_lf = GetWHOLifeData()
        return eu_lf.get_life_tables_eu()

    @property
    def gen_working_years(self) -> pd.DataFrame:
        working_years = {
            'Age': ['(15-19)', '(20-24)', '(25-29)', '(30-34)', '(35-39)', '(40-44)', '(45-49)', '(50-54)', '(55-59)',
                    '(60-64)'],
            'Mean_Age_Per_Group': [18, 22, 27, 32, 37, 42, 47, 52, 57, 62],
            'Working_Years_Left_Mean': [47, 43, 38, 33, 28, 23, 18, 13, 8, 3]
        }
        return pd.DataFrame(working_years)

    @staticmethod
    def get_pop_data(age_groups: List, sex_groups: List, mode: str = 'agg') -> pd.DataFrame:

        if mode not in ('agg', 'full'):
            raise TypeError('Incorrect Mode argument selected. Choices are "agg" and "full"')

        upper_age_bound = [age_groups.pop(age_groups.index('(85-89)'))] if '(85-89)' in age_groups else None

        eu = GetEUPopulation()
        eu.clean_up_df()

        if mode == 'agg':
            results = eu.get_agg_sex_cntry_pop(age=age_groups, sex=sex_groups)
            group_vals = ['Sex', 'Location']

        if mode == 'full':
            results = eu.eurostat_df
            group_vals = ['Sex', 'Age', 'Location']

        if upper_age_bound:
            un = GetPopUN()
            un.clean_up_df()
            un_lf = un.get_agg_sex_cntry_pop(age=upper_age_bound, sex=sex_groups)
            results = pd.concat([results, un_lf])
            results = results.groupby(group_vals, as_index=False).sum('Population')

        return results

    @staticmethod
    def merge_frames(df1, df2, merge_on):
        return df1.merge(df2, on=merge_on)

    @staticmethod
    def gen_file_name(age: List = ages_0_89, sex: List = sex, mode: str = 'PYLL'):
        age = age if len(age) == 1 else f'{age[0]}-{age[-1]}'
        return f'EU_{mode}_{age}_{sex}'

    @staticmethod
    def agg_exc_mort_yll(df, mode: str = 'PYLL'):
        agg_params = {'Excess_mortality_Mean': 'sum',
                      'Excess_mortality_fluc': 'sum',
                      f'{mode}_mean': 'sum',
                      f'{mode}_fluc': 'sum'}
        return df.groupby(['Location', 'Sex'], as_index=False).agg(agg_params)

    @staticmethod
    def add_mean_yll(df, mode: str = 'PYLL'):
        year_comp = 'Life_Expectancy' if mode == 'PYLL' else 'Working_Years_Left_Mean'
        df[f'{mode}_mean'] = df.apply(
            lambda x: x[year_comp] * x['Excess_mortality_Mean'] if x['Excess_mortality_Mean'] > 0 else 0,
            axis=1).round(1)
        df[f'{mode}_fluc'] = df.apply(
            lambda x: x[year_comp] * x['Excess_mortality_fluc'] if x[f'{mode}_mean'] > 0 else 0, axis=1).round(1)

        # Filter out negative and null PYLL
        df = df[df[f'{mode}_mean'] > 0]

        return df

    @staticmethod
    def add_avg_yll(df, mode: str = 'PYLL'):
        df[f'{mode}_AVG_MEAN'] = df.apply(lambda x: x[f'{mode}_mean'] / x['Excess_mortality_Mean'], axis=1).round(2)
        df[f'{mode}_AVG_FLUC'] = df.apply(lambda x: abs(
            (x[f'{mode}_mean'] + x[f'{mode}_fluc']) / (x['Excess_mortality_Mean'] + x['Excess_mortality_fluc']) - x[
                f'{mode}_AVG_MEAN']), axis=1).round(2)
        return df

    @staticmethod
    def add_std_mean_yll(df, mode: str = 'PYLL'):
        df[f'{mode}_STD_MEAN'] = df.apply(lambda x: (x[f'{mode}_mean'] / x['Population']) * 10 ** 5, axis=1).round(1)
        df[f'{mode}_STD_FLUC'] = df.apply(lambda x: (x[f'{mode}_fluc'] / x['Population']) * 10 ** 5, axis=1).round(1)

        return df

    @staticmethod
    def merge_mean_fluc_cols(df, mode: str = 'PYLL'):
        df[f'{mode}_mean ±'] = df[f'{mode}_mean'].round(1).map(str) + ' (±' + df[f'{mode}_fluc'].round(1).map(str) + ')'
        df[f'AVG_{mode} ±'] = df[f'{mode}_AVG_MEAN'].map(str) + ' (±' + df[f'{mode}_AVG_FLUC'].map(str) + ')'
        df[f'{mode}_STD ±'] = df[f'{mode}_STD_MEAN'].map(str) + ' (±' + df[f'{mode}_STD_FLUC'].map(str) + ')'

        return df

    def calculate_yll_all_ages(self, ages: Optional[List] = None, sexes: List = sex, mode: str = 'PYLL'):

        if mode == 'PYLL':
            ages = ages_0_89 if not ages else ages
            merge_on_lf_exc_mort = ['Age', 'Sex', 'Location']
        elif mode == 'WYLL':
            merge_on_lf_exc_mort = ['Age']
            ages = age_15_64 if not ages else ages
        else:
            raise ValueError('Invalid Mode Argument')

        yll_ages = self.get_life_exp_eu if mode == 'PYLL' else self.gen_working_years

        yll_dt = self.merge_frames(df1=yll_ages,
                                   df2=self.get_excess_mortality,
                                   merge_on=merge_on_lf_exc_mort)

        yll_dt = self.add_mean_yll(yll_dt, mode)
        yll_dt = self.agg_exc_mort_yll(yll_dt, mode)
        yll_dt = self.add_avg_yll(yll_dt, mode)

        merge_on_pop = ['Sex', 'Location']
        yll_dt = self.merge_frames(df1=yll_dt,
                                   df2=self.get_pop_data(age_groups=ages, sex_groups=sexes),
                                   merge_on=merge_on_pop)

        yll_dt = self.add_std_mean_yll(yll_dt, mode)
        yll_dt = self.merge_mean_fluc_cols(yll_dt, mode)

        return yll_dt

    @staticmethod
    def get_std_eu_pop_2013():
        # Todo: add info about static file used instead of FED_INFO_SYS
        file = 'Standard populations - Federal Health Monitoring.csv'
        file_path = path.join(source_std_eu_2013_pop_data, file)
        df = pd.read_csv(file_path)
        df['Sex'] = df.loc[:, 'Sex'].str.replace('All sexes', 'Total')
        df['Age'] = df.apply(lambda x: std_eu_pop_2013_decode_age.get(x['Age']), axis=1)
        df = df[~df['Age'].isnull()]
        df['Standard population of Europe 2013 Info'] = df['Standard population of Europe 2013 Info'].map(int)
        df = df.groupby(['Age', 'Sex'], as_index=False).sum('Standard population of Europe 2013 Info')
        return df

    def calculate_asyr(self, ages: Optional[List] = None, sexes: List = sex):

        ages = ages_0_89 if not ages else ages
        yll_ages = self.get_life_exp_eu
        yll_dt = self.merge_frames(df1=yll_ages,
                                   df2=self.get_excess_mortality,
                                   merge_on=['Age', 'Sex', 'Location'])

        yll_dt = self.add_mean_yll(yll_dt)

        yll_dt = self.merge_frames(df1=yll_dt,
                                   df2=self.get_pop_data(ages, sexes, mode='full'),
                                   merge_on=['Age', 'Sex', 'Location'])

        yll_dt = self.merge_frames(df1=yll_dt,
                                   df2=self.get_std_eu_pop_2013(),
                                   merge_on=['Age', 'Sex'])

        yll_dt['PYLL_Rate'] = yll_dt.apply(lambda x: (x['PYLL_mean'] / x['Population']) * 10 ** 5, axis=1).round(2)
        yll_dt['PYLL_Rate_fluc'] = yll_dt.apply(lambda x: (x['PYLL_fluc'] / x['Population']) * 10 ** 5, axis=1).round(2)

        yll_dt['Pop_per_100000'] = yll_dt.apply(lambda x: (x['Standard population of Europe 2013 Info'] / 99_000), axis=1).round(3)
        yll_dt['ASYR'] = yll_dt.apply(lambda x: (x['PYLL_Rate'] * x['Pop_per_100000']), axis=1).round(3)
        yll_dt['ASYR_FLUC'] = yll_dt.apply(lambda x: (x['PYLL_Rate_fluc'] * x['Pop_per_100000']), axis=1).round(3)

        agg_params = {'ASYR': 'sum',
                      'ASYR_FLUC': 'sum', }
        return yll_dt.groupby(['Location', 'Sex'], as_index=False).agg(agg_params)
