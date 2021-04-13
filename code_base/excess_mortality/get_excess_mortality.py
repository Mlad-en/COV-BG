from typing import Optional

import numpy as np

from code_base.excess_mortality.eurostat_bulk_base import GetBulkEurostatDataBase, DECODE_DEMO_COL
from code_base.excess_mortality.folder_constants import *
from code_base.utils.file_utils import *


class GetExcessMortalityCountry(GetBulkEurostatDataBase):
    def __init__(self, add_current_year: bool = False, current_year_weeks: Optional[int] = None):
        self.eurostat_data = 'excess_mortality_by_sex_age_country'
        super().__init__(self.eurostat_data, add_current_year, current_year_weeks)

    def clean_up_df(self):

        # Splits demographic data from the first column of the Eurostat dataset to separate columns,
        # i.e. split age, sex and other units into their own separate columns.
        self.split_demographic_data(
            split_from=self.split_columns['split_from_demo'],
            split_into=self.split_columns['split_into_demo'],
            separator=',')

        year_week_columns: List = self.generate_year_week_columns
        self.filter_cols(year_week_columns)

        self.eurostat_df: pd.DataFrame = self.eurostat_df.melt(id_vars=self.retain_demo_columns,
                                                               value_vars=year_week_columns,
                                                               var_name=self.split_columns['split_from_year_week'],
                                                               value_name='Mortality')

        self.split_demographic_data(
            split_from=self.split_columns['split_from_year_week'],
            split_into=self.split_columns['split_into_year_week'],
            separator='W')

        self.eurostat_df = self.eurostat_df[~self.eurostat_df['Age'].str.contains('UNK', na=False)]

        self.eurostat_df: pd.DataFrame = clean_unneeded_symbols(self.eurostat_df, ':', np.nan)
        self.eurostat_df: pd.DataFrame = clean_unneeded_symbols(self.eurostat_df, 'p', '')

        self.decode_demo_values()


class GetExcessMortalityRegion(GetBulkEurostatDataBase):

    def __init__(self, filter_country: str, add_current_year: bool = False, current_year_weeks: Optional[int] = None):
        self.eurostat_data: str = 'excess_mortality_by_sex_age_nuts3'
        self.filter_country: str = filter_country
        super().__init__(self.eurostat_data, add_current_year, current_year_weeks)

    def clean_up_df(self):
        filt_unknown_regions: List = [loc for loc in self.replace_location_name.keys() if self.filter_country in loc]

        self.eurostat_df = self.eurostat_df[self.eurostat_df[
            DECODE_DEMO_COL[self.eurostat_data]].str.contains(self.filter_country, na=False)]

        self.split_demographic_data(
            split_from=self.split_columns['split_from_demo'],
            split_into=self.split_columns['split_into_demo'],
            separator=',')

        year_week_columns: List = self.generate_year_week_columns
        self.filter_cols(year_week_columns)

        self.eurostat_df: pd.DataFrame = self.eurostat_df.melt(id_vars=self.retain_demo_columns,
                                                               value_vars=year_week_columns,
                                                               var_name=self.split_columns['split_from_year_week'],
                                                               value_name='Mortality')

        self.split_demographic_data(
            split_from=self.split_columns['split_from_year_week'],
            split_into=self.split_columns['split_into_year_week'],
            separator='W')

        self.eurostat_df = self.eurostat_df[self.eurostat_df['Location'].isin(filt_unknown_regions)]
        self.eurostat_df = self.eurostat_df[~self.eurostat_df['Age'].str.contains('UNK', na=False)]

        self.eurostat_df: pd.DataFrame = clean_unneeded_symbols(self.eurostat_df, ':', np.nan)
        self.eurostat_df: pd.DataFrame = clean_unneeded_symbols(self.eurostat_df, 'p', '')

        self.decode_demo_values()


class ExcessMortalityMapper:
    """
    This class is used to map between the GetExcessMortalityCountry and GetExcessMortalityRegion classes. As the names of
    classes suggest, one is used to invoke cross-country data, while the other provides data about regions within a specific country.
    """
    def __init__(self, cntry: str = None, add_current_year: bool = False, current_year_weeks: Optional[int] = None):
        """

        :param cntry: The country parameter controls the flow between producing excess mortality across countries
        or across regions within a country.
        :param add_current_year: Allows a potential interface for analyzing 2020 or also 2021. By default it only includes 2020.
        :param current_year_weeks: If analysis requires 2021, then the cut off week number must be specified.
        """
        self.cntry = cntry
        self.add_current_year = add_current_year
        self.current_year_weeks = current_year_weeks

    @property
    def get_data_type(self):
        """
        :return: Returns class instance depending on whether the current class has been created with a country argument or not.
        """
        if not self.cntry:
            return GetExcessMortalityCountry(add_current_year=self.add_current_year,
                                             current_year_weeks=self.current_year_weeks)
        else:
            return GetExcessMortalityRegion(filter_country=self.cntry,
                                            add_current_year=self.add_current_year,
                                            current_year_weeks=self.current_year_weeks)

    def generate_data(self) -> str:
        """
        Function creates a csv file of the mortality data for either country_dt or region.
        :return: Function returns the path to the generated file.
        """
        data = self.get_data_type
        data.clean_up_df()

        # Generate naming convention for file.
        from_range = data.generate_year_week_columns[0]
        to_range = data.generate_year_week_columns[-1]
        if self.cntry:
            file = f'{self.cntry}_excess_mortality_{from_range}_{to_range}'
        else:
            file = f'EU_excess_mortality_{from_range}_{to_range}'

        save_to_loc = source_excess_mortality_regions if self.cntry else source_excess_mortality_countries
        file_path = data.save_df_to_file(df=data.eurostat_df, location=save_to_loc, file_name=file)

        return file_path