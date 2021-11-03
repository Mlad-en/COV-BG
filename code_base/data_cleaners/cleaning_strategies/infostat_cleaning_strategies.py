from abc import abstractmethod, ABC
from typing import Dict, List

import pandas as pd

from code_base.data_cleaners.cleaning_params.infostat_params import InfostatHeaders
from code_base.data_cleaners.utilities.column_operations import split_columns_by_data
from code_base.data_cleaners.utilities.translate_values import decode_val
from code_base.data_bindings.BG_municipalities_translations import BG_MUNS_BGR_TO_ENG
from code_base.data_bindings.age_group_translations import INFOSTAT_DECODE_AGE_GROUPS


class BaseInfostatCleaningStrategy(ABC):
    """Class provides a base cleaning strategy for infostat data scraped from their website."""

    def __init__(self, dataframes: List, filter_df_by: List, col_headers: Dict, melt_cols: Dict):
        self.dataframes = dataframes
        self.filter_df_by = filter_df_by
        self.col_headers = col_headers
        self.melt_cols = melt_cols
        self.data_to_clean = pd.DataFrame()
        self.headers = InfostatHeaders

    def _filter_dfs(self) -> pd.DataFrame:
        """
        Function looks in list of data frames provided and locates the one that contains demographic data
        about Men and Women in its second to last and last column respectively.
        :return: DataFrame containing scraped infostat data depending on the file type.
        """

        women, men = self.filter_df_by
        for df in self.dataframes:
            if women in list(df.iloc[:, -1].head(10).values) and men in list(df.iloc[:, -2].head(10).values):
                return df
        else:
            raise ValueError('Could not locate demography data in any infostat df.')

    def _rename_initial_columns(self):
        """
        Function renames the initial columns (before being mutated) from basic indices [0, 1, 2, etc.] to
        more meaningful names.
        :return: Functions returns None.
        """
        self.data_to_clean.rename(columns=self.col_headers, inplace=True)

    def _drop_nan_from_col_zero(self):
        """
        Function used to drop rows containing None data in the first column of the DataFrame.
        :return: Functions returns None.
        """
        self.data_to_clean.dropna(how='any', subset=[0], axis=0, inplace=True)

    @abstractmethod
    def clean_data(self) -> pd.DataFrame:
        """
        Function used to clean a given data type file according to its specifics.
        :return: Function returns a DataFrame containing cleaned infostat data.
        """
        pass


class PopulationAgeSexRegionCleaningStrategy(BaseInfostatCleaningStrategy):

    def _translate_values(self) -> pd.DataFrame:
        """
        Function used to translate (standardize) AGE group data between Infostat and other sources.
        :return: Returns a dataframe containing translated age group values.
        """
        data_to_clean = decode_val(self.data_to_clean, self.headers.AGE, INFOSTAT_DECODE_AGE_GROUPS)
        return data_to_clean

    def _replace_values(self):
        """
        Function replaces values to facilitate combination with other datasets [standardizes location information]
        and to facilitate mathematical operations on the dataset[standardizes missing information as zero (0)].
        :return: Functions returns None.
        """
        repl_data = [
            [self.headers.LOCATION, 'Sofia (stolitsa)', 'Sofia-grad'],
            [self.headers.POPULATION, '-', '0']
        ]
        for dt in repl_data:
            self.data_to_clean[dt[0]].replace(to_replace=dt[1], value=dt[2], inplace=True)

    def clean_data(self) -> pd.DataFrame:
        self.data_to_clean = self._filter_dfs()

        self._drop_nan_from_col_zero()
        self.data_to_clean.drop(self.data_to_clean.columns[0], axis=1, inplace=True)
        self._rename_initial_columns()

        self.data_to_clean = self._translate_values()
        self.data_to_clean = self.data_to_clean.melt(**self.melt_cols)

        self._replace_values()

        # Grouping and summing across age groups since Infostat provide data for age groups 90-94, 95-99 and 100+,
        # whereas other other sources (e.g. Eurostat) go up only to 90+.
        self.data_to_clean[self.headers.POPULATION] = self.data_to_clean[self.headers.POPULATION].map(int)
        self.data_to_clean = self.data_to_clean.groupby([self.headers.LOCATION, self.headers.AGE, self.headers.SEX],
                                                        as_index=False).sum(self.headers.POPULATION)

        return self.data_to_clean


class LifeExpectancyBySexCleaningStrategy(BaseInfostatCleaningStrategy):

    def _replace_values(self):
        """
        Function used to replace age information (replace 100+ with just the number 100) to facilitate data combination.
        :return: Functions returns None.
        """
        repl_data = [
            [self.headers.AGE, '+', ''],
        ]
        for dt in repl_data:
            self.data_to_clean[dt[0]].replace(to_replace=dt[1], value=dt[2], inplace=True)

    def clean_data(self) -> pd.DataFrame:
        self.data_to_clean = self._filter_dfs()
        self._drop_nan_from_col_zero()

        self.data_to_clean.drop(self.data_to_clean.columns[0], axis=1, inplace=True)

        self._rename_initial_columns()
        # Replace 100+ with just the number 100.
        self._replace_values()

        self.data_to_clean = self.data_to_clean.melt(**self.melt_cols)

        return self.data_to_clean


class AVGLifeExpectancyBySexCleaningStrategy(BaseInfostatCleaningStrategy):

    def clean_data(self) -> pd.DataFrame:
        self.data_to_clean = self._filter_dfs()

        self._drop_nan_from_col_zero()
        self._rename_initial_columns()

        self.data_to_clean = self.data_to_clean.melt(**self.melt_cols)

        return self.data_to_clean


class MortalityByAgeSexMunicipalityCleaningStrategy(BaseInfostatCleaningStrategy):

    def _pivot_table_data(self) -> pd.DataFrame:
        """
        Function transposes the Years column into separate columns (e.g. 2015, 2016, 2017, etc.), with mortality set as
        the values for each new column.
        :return: Function returns a transposed DataFrame.
        """
        ind = [self.headers.LOCATION, self.headers.SEX]
        cols = self.headers.YEAR
        vals = self.headers.MORTALITY
        new_df = pd.pivot_table(self.data_to_clean, index=ind, columns=cols, values=vals)
        new_df.reset_index(inplace=True)
        return new_df

    def _translate_values(self) -> pd.DataFrame:
        """
        Function used to translate Bulgarian municipalities into English.
        :return: Returns a dataframe containing translated municipalities.
        """
        data_to_clean = decode_val(self.data_to_clean, self.headers.LOCATION, BG_MUNS_BGR_TO_ENG)
        return data_to_clean

    def _split_columns_by_data(self) -> pd.DataFrame:
        """
        Function used to split the YEAR_SEX column into two separate categorical columns.
        :return: Function returns a dataframe containing YEAR and SEX as two separate columns.
        """
        split_header = self.headers.YEAR_SEX
        split_into = [self.headers.YEAR, self.headers.SEX]
        sep = '-'
        data_to_clean = split_columns_by_data(self.data_to_clean, split_header, split_into, sep)
        return data_to_clean

    def clean_data(self) -> pd.DataFrame:
        self.data_to_clean = self._filter_dfs()

        self._drop_nan_from_col_zero()
        self._rename_initial_columns()

        self.data_to_clean = self._translate_values()
        self.data_to_clean = self.data_to_clean.melt(**self.melt_cols)
        self.data_to_clean = self._split_columns_by_data()
        self.data_to_clean[self.headers.MORTALITY] = self.data_to_clean[self.headers.MORTALITY].map(int)
        self.data_to_clean = self._pivot_table_data()

        return self.data_to_clean


class PopulationByMunicipalityCleaningStrategy(BaseInfostatCleaningStrategy):

    def _translate_values(self) -> pd.DataFrame:
        """
        Function used to translate Bulgarian municipalities into English.
        :return: Returns a dataframe containing translated municipalities.
        """
        data_to_clean = decode_val(self.data_to_clean, self.headers.LOCATION, BG_MUNS_BGR_TO_ENG)
        return data_to_clean

    def clean_data(self) -> pd.DataFrame:
        self.data_to_clean = self._filter_dfs()
        self._drop_nan_from_col_zero()
        self._rename_initial_columns()
        self.data_to_clean = self._translate_values()
        self.data_to_clean = self.data_to_clean.melt(**self.melt_cols)
        return self.data_to_clean
