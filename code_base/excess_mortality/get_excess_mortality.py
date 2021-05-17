from datetime import datetime
from typing import Dict, Optional, Union

from code_base.excess_mortality.decode_args import *
from code_base.excess_mortality.folder_constants import source_excess_mortality_regions, \
    source_excess_mortality_countries
from code_base.utils.file_utils import *
from code_base.excess_mortality.url_constants import *
import numpy as np


class BaseBulkEurostatData(SaveFileMixin):
    def __init__(self, eurostat_data: str,
                 zipped: bool = True):

        self.eurostat_data: str = eurostat_data

        self.split_columns: Dict = {
            'split_from_demo': DECODE_DEMO_COL[self.eurostat_data],
            'split_into_demo': DECODE_DEMO_REPL[self.eurostat_data],
            'split_by_demo': DECODE_DEMO_SEPARATOR[self.eurostat_data],
            # TODO: potentially move into MORTALITY BASE CLASS
            'split_from_year_week': 'Year_week',
            'split_into_year_week': ['Year', 'Week']
        }

        self.location_code_name = COUNTRY_REPLACE[self.eurostat_data]

        if zipped:
            self.eurostat_df: pd.DataFrame = pd.read_csv(self.url,
                                                         compression='gzip',
                                                         sep='\t',
                                                         encoding='utf-8-sig',
                                                         low_memory=False)
        else:
            self.eurostat_df: pd.DataFrame = pd.read_csv(self.url,
                                                         encoding='utf-8-sig')

        super().__init__()

    @property
    def url(self) -> str:
        """
        Property describes the API source for the dataset used.

        :return: Returns a full API string used to obtain a given dataset.
        """
        domain: str = EUROSTAT_DATA['main']
        url_path: str = EUROSTAT_DATA['files'][self.eurostat_data]
        full_url: str = domain + url_path
        return full_url

    @property
    def retain_columns(self) -> List:
        """
        Property describes columns in the dataset that should be retained.

        :return: Returns a list of columns in the dataset that should be retained.
        """
        retain_columns = RETAIN_COLUMNS[self.eurostat_data].copy()
        return retain_columns

    def split_columns_by_data(self,
                              split_from,
                              split_into,
                              separator: str) -> None:
        """
        Eurostat files are presented with sex, age and other demographic data into a single column.
        This method separates them into their own columns. Method performs this inplace and does not return anything.

        :param split_from: The column header name that needs to be split.
        :param split_into: The names of the resulting column headers.
        :param separator: The separator used to split the columns, i.e. comma "," or some other symbol.
        :return: The method does not return data. It manipulates the existing dataframe within the class instance.
        """
        col_ind = self.eurostat_df.columns.get_loc(split_from)
        self.eurostat_df[split_into] = self.eurostat_df.iloc[:, col_ind].str.split(pat=separator, expand=True)
        self.eurostat_df.drop(split_from, axis=1, inplace=True)

        return

    def filter_cols(self, filt_cols: List) -> None:
        """
        Method is used to filter out any unnecessary columns from the dataframe.
        Method should be provided only columns that must remain.

        :param filt_cols: A list of all columns that need to be retained in the DataFrame.
        :return: The method does not return data. It manipulates the existing dataframe within the class instance.
        """
        self.eurostat_df.drop(self.eurostat_df.columns[~self.eurostat_df.columns.isin(filt_cols)],
                              axis=1,
                              inplace=True)

        return

    def replace_symbols(self, symbol_to_replace: str, replace_with: Union[str, float], apply_to_cols: List) -> None:
        """
        Method replaces symbols related to data cleaning, e.g. replace ("P") values put next to mortality values.
        to signify "preliminary data" with nothing ("").

        :param symbol_to_replace: Symbol that needs to be replaced.
        :param replace_with: The symbol to be replaced with.
        :param apply_to_cols: List of columns for which the replace function is applicable.
        :return: The method does not return data. It manipulates the existing dataframe within the class instance.
        """
        self.eurostat_df[apply_to_cols] = self.eurostat_df[apply_to_cols].replace(symbol_to_replace, replace_with, regex=True)

        return

    def decode_demo_values(self) -> None:
        """
        The method transforms demographically coded values (e.g. country ISO codes) into their full value (e.g. Country name).

        :return: The method does not return data. It manipulates the existing dataframe within the class instance.
        """
        decode_demo_info = {
            'Location': self.location_code_name,
            'Sex': EUROSTAT_SEX_CONVERSION,
            'Age': EUROSTAT_AGES_CONVERSION
        }
        for key, val in decode_demo_info.items():
            self.eurostat_df[key] = self.eurostat_df.apply(lambda x: val.get(x[key], np.nan), axis=1)
            self.eurostat_df = self.eurostat_df[~self.eurostat_df[key].isnull()]

        return

    def clean_up_df(self) -> None:
        """
        Method performs clean up operations on a given dataset. It will filter columns, split columns, filter rows, etc.
        to transform the given dataset.

        :return: The method does not return data. It manipulates the existing dataframe within the class instance.
        """
        self.split_columns_by_data(
            split_from=self.split_columns['split_from_demo'],
            split_into=self.split_columns['split_into_demo'],
            separator=self.split_columns['split_by_demo'])

        self.filter_cols(self.retain_columns)

        self.decode_demo_values()

        return


class BulkEurostatMortalityData(BaseBulkEurostatData):

    def __init__(self, eurostat_data, years: List):
        self.analyze_years = years
        super().__init__(eurostat_data)

    @staticmethod
    def weeks_in_year(year: int) -> int:
        """
        Per ISO 8601,the last week of the year always contains the 28th of Dec.
        https://en.wikipedia.org/wiki/ISO_week_date#Last_week

        :param year: Year for which last week number is required
        :return: Returns the last week number for a given year (53 weeks or 52 weeks).
        """
        last_week = date(year, 12, 28)
        return last_week.isocalendar()[1]

    def include_year_week_cols(self) -> List:
        """
        The method generates a list of all years between 2015 and the current year. It then generates the week numbers for
        each year (52/53 depending for past years, depending on the year). For the current year it generates week numbers
        until the current week number of the year.

        :return: Returns a list of Year/Week for each year between 2015 and current year, in the following format:
        'YEAR<W>WEEK_NUMBER<SPACE>'
        e.g. '2020W53 '
        These strings correspond to column headers in Eurostat Mortality files.
        """
        week_years = []

        for year in self.analyze_years:
            end_range_incl = self.weeks_in_year(year) if year < datetime.today().year else datetime.today().isocalendar()[1]

            for week in range(1, end_range_incl + 1):
                week_years.append(f'{year}W{str(week).zfill(2)} ')

        return week_years

    @property
    def retain_columns(self) -> List:
        """
        Property extends the list data in the baseclass(demographic info) to include year-week column headers, specific to
        Mortality data per country/region.

        :return: Returns a list of columns in the dataset that should be retained.
        """
        retain_data = super(BulkEurostatMortalityData, self).retain_columns
        retain_data.extend(self.include_year_week_cols())
        return retain_data

    def clean_up_df(self) -> None:
        super().clean_up_df()

        # TODO: Think of way to fix id_vars so it does not reference RETAIN_COLUMNS directly.
        # TODO: Add comment explanations to the code.
        self.eurostat_df = self.eurostat_df.melt(id_vars=RETAIN_COLUMNS[self.eurostat_data],
                                                 var_name=self.split_columns['split_from_year_week'],
                                                 value_name='Mortality')

        self.split_columns_by_data(
            split_from=self.split_columns['split_from_year_week'],
            split_into=self.split_columns['split_into_year_week'],
            separator='W')

        self.replace_symbols(symbol_to_replace=':', replace_with=np.nan, apply_to_cols=['Mortality'])
        self.replace_symbols(symbol_to_replace='p', replace_with='', apply_to_cols=['Mortality'])

        self.eurostat_df = self.eurostat_df.pivot(index=['Age', 'Sex', 'Location', 'Week'], columns='Year', values='Mortality')

        self.eurostat_df.reset_index(inplace=True)

        return


class FetchExcessMortalityCountries(BulkEurostatMortalityData):
    def __init__(self, years: List):
        self.eurostat_data = 'excess_mortality_by_sex_age_country'
        self.file_location = source_excess_mortality_countries
        super().__init__(self.eurostat_data, years)


class FetchExcessMortalityRegions(BulkEurostatMortalityData):
    def __init__(self, filter_country: str, years: List):
        self.eurostat_data = 'excess_mortality_by_sex_age_nuts3'
        self.filter_country: str = filter_country
        self.file_location = source_excess_mortality_regions
        super().__init__(self.eurostat_data, years)

    def filt_country_regions(self) -> None:
        """
        Method filters out all regions other than the ones related to the instance' ISO-2 code filter_country property.

        :return: The method does not return data. It manipulates the existing dataframe within the class instance.
        """
        column_name = self.split_columns['split_from_demo']
        mask = ~self.eurostat_df[column_name].str.contains(self.filter_country)
        self.eurostat_df.drop(self.eurostat_df[mask].index, inplace=True)

        return

    def clean_up_df(self) -> None:
        # Method is overridden to filter for country regions for the given class instance's country.
        self.filt_country_regions()
        super().clean_up_df()


class ExcessMortalityMapper:
    """
    This class is used to map between the FetchExcessMortalityCountries and FetchExcessMortalityRegions classes. As the names of
    classes suggest, one is used to invoke cross-country data, while the other provides data about regions within a specific country.
    """
    def __init__(self, years: List, cntry: str = None):
        self.cntry = cntry
        self.years = years

    @property
    def get_clean_data(self):
        """The method maps between whether a specific country's regions or EU countries in general are going to be analyzed,
        depending on whether or not the class instance is created with/out country parameter. If country is specified, then
        only the country's regions are analyzed.

        :return: Returns class instance depending on whether the current class has been created with a country argument or not.
        """
        if not self.cntry:
            data = FetchExcessMortalityCountries(years=self.years)

        else:
            data = FetchExcessMortalityRegions(years=self.years, filter_country=self.cntry)

        data.clean_up_df()
        return data

    def save_clean_mort_data(self) -> str:
        """
        Function creates a csv file of the CLEANED mortality data for either EU countries or a given country's regions.

        :return: Function returns the path to the generated file.
        """

        if self.cntry:
            file = f'{self.cntry}_excess_mortality_{self.years}'
        else:
            file = f'EU_excess_mortality_{self.years}'

        file_path = self.get_clean_data.save_df_to_file(df=self.get_clean_data.eurostat_df,
                                                        location=self.get_clean_data.file_location,
                                                        file_name=file)

        return file_path