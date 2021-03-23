from typing import List, Optional

import pandas as pd

from code_base.excess_mortality.calc_excess_mortality import CalcExcessMortality
from code_base.pyll.folder_constants import output_pyll_eu
from code_base.pyll.get_who_life_data import GetWHOLifeData
from code_base.utils.common_query_params import exclude_cntrs, sex,ages_0_89, age_15_64
from code_base.excess_mortality.get_population_eu import GetPopUN

from code_base.utils.save_file_utils import SaveFile


class CalcExcessMortPyll(SaveFile):
    def __init__(self):
        self.file_location = output_pyll_eu

    @property
    def get_excess_mortality(self) -> pd.DataFrame:
        eu_mortality = CalcExcessMortality()
        mortality = eu_mortality.get_mortality_df
        exc_mort = eu_mortality.calc_excess_mortality(eu_mortality.clean_eu_data(mortality, exclude_cntrs), add_age=True)

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
    def get_un_pop_data(age_groups: List, sex_groups: List) -> pd.DataFrame:
        pop_eu = GetPopUN()
        pop_eu.clean_up_df()
        return pop_eu.get_agg_sex_cntry_pop(age=age_groups, sex=sex_groups)

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

    def calculate_yll_all_ages(self, ages: List = ages_0_89, sexes: List = sex, mode: str = 'PYLL'):

        if mode == 'PYLL':
            merge_on_lf_exc_mort = ['Age', 'Sex', 'Location']
        elif mode == 'YPPLL':
            merge_on_lf_exc_mort = ['Age']
        else:
            raise ValueError('Invalid Mode Argument')

        merge_on_pop = ['Sex', 'Location']

        yll_ages = self.get_life_exp_eu if mode == 'PYLL' else self.gen_working_years

        pyll_dt = self.merge_frames(df1=yll_ages,
                                    df2=self.get_excess_mortality,
                                    merge_on=merge_on_lf_exc_mort)

        pyll_dt = self.add_mean_yll(pyll_dt, mode)
        pyll_dt = self.agg_exc_mort_yll(pyll_dt, mode)
        pyll_dt = self.add_avg_yll(pyll_dt, mode)

        pyll_dt = self.merge_frames(df1=pyll_dt,
                                    df2=self.get_un_pop_data(age_groups=ages, sex_groups=sexes),
                                    merge_on=merge_on_pop)

        pyll_dt = self.add_std_mean_yll(pyll_dt, mode)
        pyll_dt = self.merge_mean_fluc_cols(pyll_dt, mode)

        return pyll_dt