from http.client import IncompleteRead
from os import path
from typing import List, Optional

import pandas as pd

from code_base.data_bindings.column_naming_consts import COLUMN_HEADING_CONSTS as COL_HEAD
from code_base.data_bindings.data_types import EurostatDataSets
from code_base.data_output.calc_excess_mortality import CalcExcessMortalityPredicted
from code_base.data_source.get_source_data import get_source_data
from code_base.excess_mortality.decode_args import std_eu_pop_2013_decode_age
from code_base.excess_mortality.get_pop_cntr import get_itl_pop
from code_base.pyll.folder_constants import output_pyll_eu, source_std_eu_2013_pop_data
from code_base.pyll.get_life_data import GetWHOLifeData
from code_base.utils.common_query_params import sex, ages_0_89, age_15_64, ages_all
from code_base.excess_mortality.get_population_eu import GetPopUN, GetEUPopulation

from code_base.utils.file_utils import SaveFileMixin


class CalcPYLL(SaveFileMixin):
    # TODO: Add explainer text.
    def __init__(self, over_90_included: bool = False,
                 static_lf_over_90: bool = False,
                 exclude_cntrs: Optional[List] = None,
                 analyze_year: int = 2020,
                 from_week: int = 10,
                 until_week: int = 53,
                 years: Optional[List] = None):
        """

        :param over_90_included:
        :param static_lf_over_90:
        :param exclude_cntrs:
        :param analyze_year:
        :param from_week:
        :param until_week:
        """
        self.file_location = output_pyll_eu
        self.over_90_included = over_90_included
        self.static_lf_over_90 = static_lf_over_90
        self.exclude_cntrs = exclude_cntrs
        self.analyze_year = analyze_year
        self.from_week = from_week
        self.until_week = until_week
        self.years = years

    @property
    def get_excess_mortality(self) -> pd.DataFrame:
        """

        :return:
        """

        mort_type = EurostatDataSets.MORTALITY_BY_SEX_AGE_COUNTRY
        eu_mort_data = get_source_data(mort_type, analyze_years=self.years)
        excess_mort = CalcExcessMortalityPredicted(data_type=mort_type, all_years=self.years)
        calc_mort = excess_mort.calculate(eu_mort_data, ages_all, sex, self.from_week, group_by='all')
        relevant_cols = [COL_HEAD.AGE, COL_HEAD.SEX, COL_HEAD.LOCATION,
                         COL_HEAD.EXCESS_MORTALITY_BASE, COL_HEAD.CONFIDENCE_INTERVAL, COL_HEAD.IS_SIGNIFICANT]
        calc_mort.drop(columns=[col for col in calc_mort if col not in relevant_cols], inplace=True)

        return calc_mort

    @property
    def get_life_exp_eu(self) -> pd.DataFrame:
        """

        :return:
        """

        # While loop used since there are intermittent issues with data collection from Eurostat with this particular dataset.
        while True:
            try:
                eu_lf = GetWHOLifeData()
                df = eu_lf.get_life_tables_eu(add_90_and_over=self.over_90_included,
                                              static_over_90=self.static_lf_over_90)
                break
            except IncompleteRead:
                continue

        return df

    @property
    def gen_working_years(self) -> pd.DataFrame:
        """

        :return:
        """

        working_years = {
            'Age': ['(15-19)', '(20-24)', '(25-29)', '(30-34)', '(35-39)', '(40-44)', '(45-49)', '(50-54)', '(55-59)',
                    '(60-64)'],
            'Mean_Age_Per_Group': [17.5, 22.5, 27.5, 32.5, 37.5, 42.5, 47.5, 52.5, 57.5, 62.5],
            'Working_Years_Left_Mean': [47, 42.5, 37.5, 32.5, 27.5, 22.5, 17.5, 12.5, 7.5, 2.5]
        }
        return pd.DataFrame(working_years)

    @staticmethod
    def get_pop_data(age_groups: List, sex_groups: List, mode: str = 'agg') -> pd.DataFrame:
        """

        :param age_groups:
        :param sex_groups:
        :param mode:
        :return:
        """

        if mode not in ('agg', 'full'):
            raise TypeError('Incorrect Mode argument selected. Choices are "agg" and "full"')

        upper_age_bound = [age_group for age_group in age_groups if age_group in ('(85-89)', '(90+)')]
        age_groups = [age_group for age_group in age_groups if age_group not in ('(85-89)', '(90+)')]

        while True:
            try:
                eu = GetEUPopulation()
                eu.clean_up_df()
                break
            except IncompleteRead:
                continue

        if mode == 'agg':
            results = eu.get_agg_sex_cntry_pop(age=age_groups, sex=sex_groups)
            group_vals = ['Sex', 'Location']
            drop_age = True

        elif mode == 'full':
            results = eu.eurostat_df
            group_vals = ['Sex', 'Age', 'Location']
            drop_age = False

        # Supplement data for the 85-89 and 90+ age groups. Eurostat data only goes up to 85+. To account for this
        # use data form the UN Data Services for these ranges. For all EU countries age ranges are 85-89, 90-94, 95-99, 100+.
        # This requires a translation from 90-94, 95-99, 100+ --to--> 90+.
        # Furthermore, the UN data set is missing information about the UK and Italy. For Italy, supplement data from demo.istat.it
        if upper_age_bound:
            un = GetPopUN()
            un.clean_up_df()
            un_lf = un.get_agg_sex_cntry_pop(age=upper_age_bound, sex=sex_groups, drop_age=drop_age)
            results = pd.concat([results, un_lf])
            results = results.groupby(group_vals, as_index=False).sum('Population')
            it_pop = get_itl_pop(age_range=upper_age_bound)
            results = pd.concat([results, it_pop])
            results = results.groupby(group_vals, as_index=False).sum('Population')

        return results

    @staticmethod
    def merge_frames(df1, df2, merge_on):
        """

        :param df1:
        :param df2:
        :param merge_on:
        :return:
        """

        return df1.merge(df2, on=merge_on)

    @staticmethod
    def agg_exc_mort_yll(df, mode: str = 'PYLL'):
        """

        :param df:
        :param mode:
        :return:
        """
        agg_params = {COL_HEAD.EXCESS_MORTALITY_BASE: 'sum',
                      COL_HEAD.CONFIDENCE_INTERVAL: 'sum',
                      f'{mode}_mean': 'sum',
                      f'{mode}_fluc': 'sum'}
        return df.groupby(['Location', 'Sex'], as_index=False).agg(agg_params)

    @staticmethod
    def add_mean_yll(df, mode: str = 'PYLL'):
        """

        :param df:
        :param mode:
        :return:
        """
        year_comp = 'Life_Expectancy' if mode == 'PYLL' else 'Working_Years_Left_Mean'
        df[f'{mode}_mean'] = df.apply(
            lambda x: x[year_comp] * x[COL_HEAD.EXCESS_MORTALITY_BASE] if x[COL_HEAD.EXCESS_MORTALITY_BASE] > 0 else 0,
            axis=1).round(1)
        df[f'{mode}_fluc'] = df.apply(
            lambda x: x[year_comp] * x[COL_HEAD.CONFIDENCE_INTERVAL] if x[f'{mode}_mean'] > 0 else 0, axis=1).round(1)

        # Filter out negative and null PYLL
        df = df[df[f'{mode}_mean'] > 0]

        return df

    @staticmethod
    def add_avg_yll(df, mode: str = 'PYLL'):
        """

        :param df:
        :param mode:
        :return:
        """

        df[f'{mode}_AVG_MEAN'] = df.apply(lambda x: x[f'{mode}_mean'] / x[COL_HEAD.EXCESS_MORTALITY_BASE], axis=1).round(2)
        df[f'{mode}_AVG_FLUC'] = df.apply(lambda x: abs(
            (x[f'{mode}_mean'] + x[f'{mode}_fluc']) / (x[COL_HEAD.EXCESS_MORTALITY_BASE] + x[COL_HEAD.CONFIDENCE_INTERVAL]) - x[
                f'{mode}_AVG_MEAN']), axis=1).round(2)
        return df

    @staticmethod
    def add_std_mean_yll(df, mode: str = 'PYLL'):
        """

        :param df:
        :param mode:
        :return:
        """

        df[f'{mode}_STD_MEAN'] = df.apply(lambda x: (x[f'{mode}_mean'] / x['Population']) * 10 ** 5, axis=1).round(1)
        df[f'{mode}_STD_FLUC'] = df.apply(lambda x: (x[f'{mode}_fluc'] / x['Population']) * 10 ** 5, axis=1).round(1)

        return df

    @staticmethod
    def merge_mean_fluc_cols(df, mode: str = 'PYLL'):
        """

        :param df:
        :param mode:
        :return:
        """
        df[f'{mode}_mean ±'] = df[f'{mode}_mean'].round(1).map(str) + ' (±' + df[f'{mode}_fluc'].round(1).map(str) + ')'
        df[f'AVG_{mode} ±'] = df[f'{mode}_AVG_MEAN'].map(str) + ' (±' + df[f'{mode}_AVG_FLUC'].map(str) + ')'
        df[f'{mode}_STD ±'] = df[f'{mode}_STD_MEAN'].map(str) + ' (±' + df[f'{mode}_STD_FLUC'].map(str) + ')'

        return df

    def calculate_yll_all_ages(self, ages: Optional[List] = None, sexes: List = sex, mode: str = 'PYLL'):
        """

        :param ages:
        :param sexes:
        :param mode:
        :return:
        """
        if mode == 'PYLL':
            ages = ages_0_89 if not ages else ages
            merge_on_lf_exc_mort = [COL_HEAD.AGE, COL_HEAD.SEX, COL_HEAD.LOCATION]
        elif mode == 'WYLL':
            merge_on_lf_exc_mort = [COL_HEAD.AGE]
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

        merge_on_pop = [COL_HEAD.SEX, COL_HEAD.LOCATION]
        yll_dt = self.merge_frames(df1=yll_dt,
                                   df2=self.get_pop_data(age_groups=ages, sex_groups=sexes),
                                   merge_on=merge_on_pop)

        yll_dt = self.add_std_mean_yll(yll_dt, mode)
        yll_dt = self.merge_mean_fluc_cols(yll_dt, mode)

        return yll_dt

    @staticmethod
    def get_std_eu_pop_2013():
        """

        :return:
        """
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

    def calculate_asyr(self, ages: Optional[List] = None, sexes: List = sex) -> pd.DataFrame:
        """
        Function is used to calculate ASYR (Age-Standardized Years of Life Lost Rate) as described in
        https://academic.oup.com/ije/article/48/4/1367/5281229?login=true.
        Limitation of function: due to the data provided by the WHO for life expectancy (data goes up to 85+)
        and the fact that data about mortality provided by Eurostat goes up to 90+, the two data sets are of unequal length.
        To account for this, calculations have been split - it could either count:
        1. Include the 90+ group for the analysis. If included, then two options are present:
        1.1. Assign the same life expectancy to the group.
        1.2. Provide a static value.
        2. Exclude the 90+ group and perform calculations from ages 0 to 89, where the 85+ life expectancy from WHO
        is applied to the 85-89 age group from Eurostat's mortality data - this is the default behavior of the function.
        :param ages: If age groups are not specified then then age groups analyzed is from ages 0 to 89.
        :param sexes: If sex group is not specified then the function will analyze it through all available groups (Male, Female, Total).
        :return: Returns a dataframe object containing ASYR calculations based on a standardized population.
        """

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

        # If calculating only under 90+ years, then since the weight of the group is 1000, it should be 100,000 - 1000
        # This is based on the "Standard populations used for age standardization in the information system of the
        # Federal Health Monitoring. Classification: age, sex, type of standard population" dataset provided by
        # The Information System of the Federal Health Monitoring, Germany.
        # They attribute 1000 people as the standard population per 10^5 people in Europe.
        # If the 90+ group is excluded then, 1000 people must be subtracted from the standard population.
        division_pop = 99_000 if not self.over_90_included else 100_000

        yll_dt['Pop_per_100000'] = yll_dt.apply(lambda x:
                                                (x['Standard population of Europe 2013 Info'] / division_pop),
                                                axis=1).round(3)
        yll_dt['ASYR'] = yll_dt.apply(lambda x: (x['PYLL_Rate'] * x['Pop_per_100000']), axis=1).round(3)
        yll_dt['ASYR_FLUC'] = yll_dt.apply(lambda x: (x['PYLL_Rate_fluc'] * x['Pop_per_100000']), axis=1).round(3)

        agg_params = {'ASYR': 'sum',
                      'ASYR_FLUC': 'sum', }
        return yll_dt.groupby(['Location', 'Sex'], as_index=False).agg(agg_params)

    def gen_file_name(self, age: List = ages_0_89, sex: List = sex, mode: str = 'PYLL', more_info: str = '') -> str:
        """
        Purpose of function is to generate file name which is product of the class'
        :param age: The groups that are included in the analysis.
        If a single age group is selected, then it will display only that age group (e.g. ['40-44']
        If multiple groups are selected, depending on whether the class is generated with the over_90 age group included:
        If included: then All_age_groups is displayed.
        If NOT included: then the first and last groups are listed (e.g. age: ['40-44','45-49', '50-54'] then it will display
        '(40-44) - (50-54)'
        :param sex: The sex groups included in the file analysis (e.g. Female and/or Male and/or Total)
        :param mode: The type of analysis that is the product of the file - PYLL, WYLL, ASYR, etc.
        :param more_info: Additional notes about the data used to produce the file.
        :return: Returns a string used to name files generated by the class' output in the following format:
        EU_<PYLL (default)|ASYR|WYLL>_<AGE_GROUP(s)>_<SEX_GROUPS>[ADDITIONAL_INFORMATION: optional]
        """
        age = age if len(age) == 1 else 'All_age_groups' if self.over_90_included else f'{age[0]}-{age[-1]}'
        return f'EU_{mode}_{age}_{sex}{more_info}'


if __name__ == '__main__':

    # Calculate PYLL and ASYR without 90+ age group
    c = CalcPYLL(years=[2015, 2016, 2017, 2018, 2019, 2020])
    pyll = c.calculate_yll_all_ages()
    c.save_df_to_file(pyll, c.file_location, c.gen_file_name(), method='excel')
    wyll = c.calculate_yll_all_ages(ages=age_15_64, mode='WYLL')
    c.save_df_to_file(wyll, c.file_location, c.gen_file_name(age=age_15_64, mode='WYLL'), method='excel')
    asyr = c.calculate_asyr()
    c.save_df_to_file(asyr, c.file_location, c.gen_file_name(mode='ASYR'), method='excel')

    # Calculate PYLL and ASYR with 90+ age group with data for 85+ provided by the WHO
    c = CalcPYLL(over_90_included=True, years=[2015, 2016, 2017, 2018, 2019, 2020])
    pyll = c.calculate_yll_all_ages(ages=ages_all)
    c.save_df_to_file(pyll, c.file_location, c.gen_file_name(), method='excel')
    asyr = c.calculate_asyr(ages=ages_all)
    c.save_df_to_file(asyr, c.file_location, c.gen_file_name(mode='ASYR'), method='excel')

    # Calculate PYLL and ASYR with 90+ age group with static life expectancy data for 90+ (4 years; hard-coded)
    c = CalcPYLL(over_90_included=True, static_lf_over_90=True, years=[2015, 2016, 2017, 2018, 2019, 2020])
    pyll = c.calculate_yll_all_ages(ages=ages_all)
    c.save_df_to_file(pyll, c.file_location, c.gen_file_name(more_info='_static_over_90'), method='excel')
    asyr = c.calculate_asyr(ages=ages_all)
    c.save_df_to_file(asyr, c.file_location, c.gen_file_name(mode='ASYR', more_info='_static_over_90'), method='excel')