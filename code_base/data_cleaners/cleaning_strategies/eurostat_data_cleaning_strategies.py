from abc import ABC, abstractmethod

from code_base.data_cleaners.utilities.filter_data import filter_columns, filter_rows_containing_string
from code_base.data_cleaners.utilities.column_operations import split_columns_by_data, convert_cols_to_rows
from code_base.data_cleaners.utilities.string_operations import replace_symbols, strip_spaces
from code_base.data_cleaners.utilities.time_functions import generate_week_years
from code_base.data_cleaners.utilities.translate_values import decode_demo_values
from code_base.data_bindings.column_naming_consts import COLUMN_HEADING_CONSTS as COL_HEAD


class EurostatBaseCleaningStrategy(ABC):

    def __init__(self, data_to_clean, **kwargs):
        self.bindings = kwargs
        self.data_to_clean = data_to_clean
        self.split_from_column = self.bindings['split_from_column']
        self.split_into_columns = self.bindings['split_into_columns']
        self.separator = self.bindings['separator']
        self.columns_to_retain = self.bindings['filter_cols']
        self.translate_values = self.bindings['translate_values']
        self.replace_values = self.bindings['replace_values']

    def _strip_spaces_from_cols(self):
        self.data_to_clean.columns = strip_spaces(self.data_to_clean.columns)

    def _split_columns_by_data(self, split_from, split_into, separator):
        data_to_clean = split_columns_by_data(self.data_to_clean,
                                              split_from,
                                              split_into,
                                              separator)
        return data_to_clean

    def _filter_columns(self, columns_to_retain):
        data_to_clean = filter_columns(self.data_to_clean, columns_to_retain)
        return data_to_clean

    def _decode_demo_values(self):
        data_to_clean = decode_demo_values(self.data_to_clean, self.translate_values)
        return data_to_clean

    @abstractmethod
    def _replace_symbols(self):
        pass

    @abstractmethod
    def clean_data(self):
        pass


class EurostatExcessMortalityCleaningStrategy(EurostatBaseCleaningStrategy):

    def __init__(self, data_to_clean, **kwargs):
        self.bindings = kwargs
        self.analyze_years = self.bindings['analyze_years']
        super().__init__(data_to_clean, **kwargs)

    def additional_filter_columns(self):
        include_cols = generate_week_years(self.analyze_years)
        columns_to_retain = self.columns_to_retain.copy()
        columns_to_retain.extend(include_cols)
        return columns_to_retain

    def _replace_symbols(self):
        data_to_clean = self.data_to_clean.copy()
        for replace_old, replace_with_new in self.replace_values:
            data_to_clean = replace_symbols(self.data_to_clean, replace_old, replace_with_new, [COL_HEAD.MORTALITY])
        return data_to_clean

    def _convert_cols_to_rows(self):
        cols_to_rows = self.split_from_column['time_period']
        data_to_clean = convert_cols_to_rows(self.data_to_clean,
                                             self.columns_to_retain,
                                             cols_to_rows,
                                             COL_HEAD.MORTALITY)
        return data_to_clean

    def clean_data(self):
        self._strip_spaces_from_cols()

        self.data_to_clean = self._split_columns_by_data(self.split_from_column['demography'],
                                                         self.split_into_columns['demography'],
                                                         self.separator['demography'])

        self.data_to_clean = self._filter_columns(self.additional_filter_columns())

        self.data_to_clean = self._decode_demo_values()

        self.data_to_clean = self._convert_cols_to_rows()

        self.data_to_clean = self._split_columns_by_data(self.split_from_column['time_period'],
                                                         self.split_into_columns['time_period'],
                                                         self.separator['time_period'])

        self.data_to_clean[COL_HEAD.YEAR] = self.data_to_clean.loc[:, COL_HEAD.YEAR].astype(int, errors='ignore')

        self.data_to_clean = self._replace_symbols()

        self.data_to_clean = self.data_to_clean.pivot(index=[COL_HEAD.AGE, COL_HEAD.SEX, COL_HEAD.LOCATION, COL_HEAD.WEEK],
                                                      columns=COL_HEAD.YEAR,
                                                      values=COL_HEAD.MORTALITY)


        self.data_to_clean.reset_index(inplace=True)

        return self.data_to_clean


class EurostatRegionExcessMortalityCleaningStrategy(EurostatExcessMortalityCleaningStrategy):
    def __init__(self, data_to_clean, **kwargs):
        self.bindings = kwargs
        self.region = self.bindings['region']
        super().__init__(data_to_clean, **kwargs)

    def clean_data(self):
        self.data_to_clean = filter_rows_containing_string(self.data_to_clean,
                                                           self.split_from_column['demography'],
                                                           self.region)
        return super().clean_data()


class EurostatEUPopulationCleaningStrategy(EurostatBaseCleaningStrategy):

    def __init__(self, data_to_clean, **kwargs):
        super().__init__(data_to_clean, **kwargs)

    def _replace_symbols(self):
        data_to_clean = self.data_to_clean.copy()
        for replace_old, replace_with_new in self.replace_values:
            data_to_clean = replace_symbols(self.data_to_clean, replace_old, replace_with_new, [COL_HEAD.POPULATION])
        return data_to_clean

    def clean_data(self):
        self._strip_spaces_from_cols()

        self.data_to_clean = self._split_columns_by_data(self.split_from_column['demography'],
                                                         self.split_into_columns['demography'],
                                                         self.separator['demography'])

        self.data_to_clean = self._filter_columns(self.columns_to_retain)

        self.data_to_clean = self._decode_demo_values()

        self.data_to_clean.rename(columns={'2020': COL_HEAD.POPULATION}, inplace=True)

        self.data_to_clean = self._replace_symbols()

        self.data_to_clean.dropna(how='any', subset=[COL_HEAD.LOCATION, COL_HEAD.POPULATION], axis=0, inplace=True)

        self.data_to_clean[COL_HEAD.POPULATION] = self.data_to_clean[COL_HEAD.POPULATION].map(int)

        return self.data_to_clean
