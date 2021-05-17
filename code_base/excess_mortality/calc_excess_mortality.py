import os
from http.client import IncompleteRead
from typing import Callable, Dict, List, Optional, Union
from functools import cached_property

import pandas as pd

from code_base.excess_mortality.base_calc_excess import ExcessMortBase
from code_base.excess_mortality.folder_constants import (output_excess_mortality_countries,
                                                         output_excess_mortality_regions,
                                                         )
from code_base.excess_mortality.get_excess_mortality import ExcessMortalityMapper
from code_base.utils.file_utils import SaveFileMixin


class FilterMortData:
    def __init__(self,
                 analyze_year: Union[str, int],
                 exclude_locations: Optional[List] = None,
                 from_week: Optional[int] = None,
                 until_week: Optional[int] = None):
        self.analyze_year = int(analyze_year)
        self.exclude_locations = exclude_locations
        self.from_week = from_week
        self.until_week = until_week

    def filter_start_week(self, df) -> pd.DataFrame:
        """
        The method is used to filter out weeks less than the from_week property, if provided. Otherwise default value is used:
        for 2020: week 10 (often considered the start of the Covid-19 pandemic in Europe), for other years: week 1.

        :param df: Dataframe object to be filtered.
        :return: The method returns a dataframe, excluding weeks less than the from_week property.
        """
        default_start = {
            2020: 10,
        }
        gte_week = self.from_week if self.from_week else default_start.get(self.analyze_year, 1)

        return df.drop(df[df['Week'].lt(gte_week)].index, axis=0)

    def filter_end_week(self, df) -> pd.DataFrame:
        """
        The method is used to filter out weeks less than the until_week property, if provided. Otherwise, the last column
        is used and missing data values are dropped. It is assumed only future weeks are dropped.

        :param df: Dataframe object to be filtered.
        :return: The method returns a dataframe, excluding weeks greater than the until_week property. If not provided,
        it drops missing values.
        """
        if self.until_week:
            return df.drop(df[df['Week'].gt(self.until_week)].index, axis=0)
        else:
            return df.dropna(subset=[df.columns[-1]], how='any', axis=0)

    def filter_out_locations(self, df) -> pd.DataFrame:
        """
        :param df: Dataframe object to be filtered.
        :return: The method returns a dataframe, excluding locations listed in the exclude_locations property.
        """
        return df.drop(df[df['Location'].isin(self.exclude_locations)].index, axis=0)

    @staticmethod
    def filter_out_blank_dt(df) -> pd.DataFrame:
        """
        :param df: Dataframe object to be filtered.
        :return: The method returns a dataframe, excluding any missing values for the last column - the year to be analysed.
        """
        return df.dropna(subset=[df.columns[-1]], how='any', axis=0)

    def filter_weeks_locations(self, df):
        df = self.filter_start_week(df)
        df = self.filter_end_week(df)
        if self.exclude_locations:
            df = self.filter_out_locations(df)
        df = self.filter_out_blank_dt(df)

        return df

    @staticmethod
    def filter_demo_data(df: pd.DataFrame, demo_type: str, demo_range: Optional[List] = None) -> pd.DataFrame:
        """
        The method return a dataframe, filtering out sex/age groups NOT specified in the demo_range parameter.

        :param df: Dataframe object to be filtered.
        :param demo_type: The demographic information type the dataframe needs to be filtered on.
        :param demo_range: Defines a list of demographic information (e.g. sex - Male, female and/or Total)
        that need to remain in the dataframe.
        :return: Returns a dataframe object, filtered by demographic information.
        """
        demo_type = demo_type
        return df.drop(df[~df[demo_type].isin(demo_range)].index, axis=0)

    def filter_all_demo_data(self, df: pd.DataFrame, demo_type_range_dict: Dict) -> pd.DataFrame:
        """
        The method return a dataframe, filtering out row data.
        :param df: Dataframe object to be filtered.
        :param demo_type_range_dict: A demographic key and range value (list of values) pair that is to remain in the df.
        :return: Returns a dataframe object, filtered by all demographic information types available.
        """
        for demo_type, demo_range in demo_type_range_dict.items():
            df = self.filter_demo_data(df, demo_type=demo_type, demo_range=demo_range)

        return df


class DataInformation:
    @staticmethod
    def per_group_info(df: pd.DataFrame):
        """
        The method adds information about the week count, minimum week number and maximum week number for each Age-Sex-Location
        group within a given dataframe. This weekly information is used as meta-data to validate excess mortality calculations.

        :return: The method does not return data. It manipulates the existing dataframe within the class instance.
        """
        week_stats = df.groupby(['Age', 'Sex', 'Location'], as_index=False).agg({'Week': ['count', 'min', 'max']})
        # Joins column headers that are separated by different levels as a result of the aggregation function above, i.e.
        # ('Week','count') becomes 'Week_count', etc.
        week_stats.columns = ['_'.join(x) if x[1] else x[0] for x in week_stats.columns]
        week_stats.drop_duplicates(inplace=True)

        return week_stats.sort_values(by=['Location', 'Sex', 'Age'], ascending=True)


class SetUpData:
    def __init__(self, is_weekly: bool = False, is_age_agg: bool = True):
        self.is_weekly = is_weekly
        self.is_age_agg = is_age_agg
        self.all_demo_values = ('Age', 'Sex', 'Location', 'Week')

    @staticmethod
    def back_fill_missing_weekly(df: pd.DataFrame) -> pd.DataFrame:
        """For all years which have only 52 weeks, copy mortality for week 52 to week 53.
        This is similar to the way it is handled in https://ourworldindata.org/excess-mortality-covid,
        where they all together compare data from week 52 for all previous years (End-note #5)."""

        return df.fillna(method='pad')

    def dec_mean_mort_calc(self, func) -> Callable:
        """
        Decorator method is used to set up mean mortality and sum values around it, depending on grouping parameters.
        :param func: Receives the mean mortality function.
        :return: Returns inner function reference.
        """

        def inner(df, *args) -> pd.DataFrame:
            """
            The grouping parameters can be Age and/or Week depending on the class instance' properties: is_weekly and
            is_age_agg.
            If is_weekly is True, Weekly values are padded when data is missing - e.g. in the cases where a year has 52 weeks,
            instead of 53. In this such cases week 53 for this year is padded by the value from the previous week - 52. All
            data is then averaged across base years
            If is_weekly is False, a mean value is derived for the amount of existing data points - i.e. if data is present
            for a single base year for mean mortality then only it will be used to calculate the mean mortality for this
            period.
            Once mean mortality is calculated, it can be summed up across Age and/or Week  for is_weekly and is_age_agg
            values respectively.
            :param df: Dataframe object to be modified with Mean Mortality.
            :param args: Mean Mortality function required parameters.
            :return: Returns a dataframe object that has been modified to include mean mortality and aggregated depending
            on class instance' values.
            """
            group_all_values = [val for val in self.all_demo_values]
            exclude_params = []

            if self.is_weekly:
                df = self.back_fill_missing_weekly(df=df)

            df = func(df, *args)

            if self.is_age_agg:
                exclude_params.append('Age')

            if not self.is_weekly:
                exclude_params.append('Week')

            group_values = [val for val in group_all_values if val not in exclude_params]

            df = df.drop(exclude_params, axis=1)
            df = df.groupby(group_values, as_index=False).sum()

            return df

        return inner


class CalcExcessMortality(SaveFileMixin):

    def __init__(self,
                 analyze_year: int,
                 from_week: int = None,
                 until_week: int = None,
                 cntry: str = None,
                 exclude_locations: Optional[List] = None):
        self.analyze_year = int(analyze_year)
        self.cntry = cntry
        self.data_info = None
        self.file_loc_base = output_excess_mortality_regions if self.cntry else output_excess_mortality_countries
        self.file_loc = os.path.join(self.file_loc_base, str(self.analyze_year))

        self.filters = FilterMortData(analyze_year=analyze_year,
                                      from_week=from_week,
                                      until_week=until_week,
                                      exclude_locations=exclude_locations)

        self.exc_mort_calcs = ExcessMortBase(analyze_year=analyze_year)

        super().__init__()

    @property
    def base_compare_years(self):
        """
        :return: Property used to return a list of years that analyzed year mortality is compared to. They provide the
        mean ranges over which excess mortality can be calculated. For the purposes of this project these are the last
        five years prior to the pandemic.
        """
        return [year for year in range(2015, 2019 + 1)]

    @property
    def include_years(self):
        """
        :return: Property returns a list of years to be included from the EU mortality's database.
        The period 2015-2019 is always included.
        The list is then supplemented with the analyze_year property of the given class instance.
        """
        always_included = [year for year in self.base_compare_years]
        always_included.append(self.analyze_year)

        return always_included

    @property
    def fetch_data_loc(self) -> str:
        """
        Property calls class that makes an API call to the Eurostat's Bulk data service for the period 2015-2019 and the
        analyze_year property for the given class instance (e.g. 2020).
        Depending on whether a particular country is being analyzed or all countries in the EU, the class proceeds accordingly.
        Finally, the dataframe is cleaned and saved locally. The property returns the file's location.

        :return: The property returns the location of a file that contains information about mortality between weekly and yearly
        periods within the EU.
        """
        while True:
            try:
                data = ExcessMortalityMapper(cntry=self.cntry, years=self.include_years)
                loc = data.save_clean_mort_data()
                break
            except IncompleteRead:
                continue

        return loc

    @cached_property
    def mortality_df(self):
        """
        :return: Property reads file returned from the fetch_data_loc property and returns a dataframe object of its contents.
        """
        data = pd.read_csv(self.fetch_data_loc, encoding='utf-8-sig')
        data = self.filters.filter_weeks_locations(df=data)
        return data

    def filter_demographic_data(self, df, age_range: Optional[List] = None, sexes: Optional[List] = None) -> pd.DataFrame:
        """
        The method return a dataframe, filtering out demographic groups. Available demographic groups are Sex and Age.
        If None is passed for either parameter, the default behavior will be to filter out everything different than 'Total'
        :param df: dataframe object to be filtered.
        :param age_range: A list of age ranges to remain in the dataframe (e.g. ['(40-44)', '(45-49)'])
        :param sexes: A list of sex groups to remain in the dataframe (e.g. ['Male', 'Female'])
        :return: Returns a dataframe, filtering out demographic groups.
        """
        age_range = age_range if age_range else ['Total']
        sexes = sexes if sexes else ['Total']
        demo_ranges = {
            'Age': age_range,
            'Sex': sexes
        }

        df = self.filters.filter_all_demo_data(df=df, demo_type_range_dict=demo_ranges)

        return df

    def calc_excess_mort(self,
                         age_range: Optional[List] = None,
                         sexes: Optional[List] = None,
                         is_weekly: bool = False,
                         is_age_agg: bool = True) -> pd.DataFrame:
        """
        Method is used to calculate excess mortality for given regions/countries depending on the class' instance'
        cntry attribute - if none is presented, then calculation is done across European countries.
        If present, then calculation is done across country' NUTS regions.
        The analysis includes comparison between a base mortality avarage (2015-2019) against the analyze_year attribute
        for the class instance (e.g. 2020).
        :param age_range: Range of age groups to be included in analysis - e.g. ['(40-44)', '(45-49)'] will only include
        age groups between 40 and 49. If not provided, It will default to 'Total'
        :param sexes: Range of sex groups to be included in analysis - e.g. ['Male', 'Female'] will only include
        sex groups Male and Female. If not provided, It will default to 'Total'.
        :param is_weekly: Describes whether data should be aggregated across weeks or should be presented in a per week format.
        :param is_age_agg: Describes whether data should be aggregated across age groups
        or should be presented in a per age group format.
        :return: Returns a dataframe object that contains excess mortality calculations e.g.:
        confidence intervals, mean mortality, excess mortality, p-scores and formatted columns for
        mean mortality (mean mortality ± confidence intervals),
        excess mortality (excess mortality ± confidence intervals),
        p-scores (p-scores ± confidence intervals).
        """

        mortality_df = self.filter_demographic_data(df=self.mortality_df, age_range=age_range, sexes=sexes)

        # Add information about the data used to generate calculations following filtration.
        # Particularly useful for 2021 where information between different countries/regions is not provided at the same time.
        # Used as both a sanity check and source verification.
        self.data_info = DataInformation().per_group_info(df=mortality_df)

        set_up = SetUpData(is_weekly=is_weekly, is_age_agg=is_age_agg)

        @set_up.dec_mean_mort_calc
        def add_mean_mort(df, years):
            return self.exc_mort_calcs.add_mean_mort(df, years)

        mortality_df = add_mean_mort(mortality_df, [str(year) for year in self.base_compare_years])
        mortality_df = self.exc_mort_calcs.add_exc_mort_info(mortality_df,
                                                             [str(year) for year in self.base_compare_years],
                                                             False)

        return mortality_df

    @staticmethod
    def df_for_multisheet_save(df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """
        The method is used to set up a dataframe object to be saved into different sheets in the same excel file.
        :param df: Dataframe object that needs to be split into multiple dataframes.
        :return: Returns a dictionary mapping between the sheet_name and dataframe objects.
        """
        dfs_dct = {sheet_name: data for sheet_name, data in df.groupby(['Sex'])}
        return dfs_dct

    def set_up_df_for_multisheet_save(self, df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """
        Splits up dataframe into a dictionary of dataframe objects that can be saved into multiple sheets in the same excel
        spreadsheet. Method also adds meta data about the information used to generate the output data and saves it in a
        new sheet called Data_Used.
        :param df: Dataframe object that needs to be split into multiple dataframes.
        :return: Returns a dictionary mapping between the sheet_name and dataframe objects with additional meta information.
        """
        data = self.df_for_multisheet_save(df=df)
        if self.data_info is not None:
            data['Data_Used'] = self.data_info
        return data

    def get_file_naming_convention(self,
                                   age_lst: Optional[List] = None,
                                   sex: Optional[List] = None,
                                   weekly: bool = False,
                                   age_agg: bool = True) -> str:
        """
        Method generates the file naming convention for output files generated by the calc_excess_mort method of the class.
        :param age_lst: The age range used for the calc_excess_mort calculation.
        :param sex: The sex groups used for the calc_excess_mort calculation.
        :param weekly: Whether calculations are aggregated across weeks or are per week.
        :param age_agg: Whether calculations are aggregated across age groups or are per age groups.
        :return: Returns a string containing the resulting file name.
        """
        year = self.analyze_year

        time_period = 'WEEKLY' if weekly else 'TOTAL'
        cntry = self.cntry if self.cntry else 'EU'
        sex = f'{sex}' if sex else f'(SEX-TOTAL)'
        age_agg = 'AGE_AGGREGATED' if age_agg else 'BY_AGE_GROUP'

        if age_lst and len(age_lst) > 1:
            age = f'{age_lst[0]} - {age_lst[-1]}'
        elif age_lst:
            age = f'{age_lst[0]}'
        else:
            age = f'(AGE-TOTAL)'

        file_name = f'{year}_{age_agg}_{time_period}_{cntry}_{sex}_{age}'

        return file_name