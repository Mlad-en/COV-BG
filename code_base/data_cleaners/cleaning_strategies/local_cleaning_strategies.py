from abc import ABC, abstractmethod

import pandas as pd

from code_base.data_cleaners.cleaning_params.local_cleaning_params import ItalyPopDataHeaders, StandardPopHeaders
from code_base.data_cleaners.utilities.column_operations import convert_cols_to_rows
from code_base.data_cleaners.utilities.filter_data import filter_columns
from code_base.data_cleaners.utilities.translate_values import decode_demo_values


class LocalBaseCleaningStrategy(ABC):

    @abstractmethod
    def clean_data(self):
        pass


class UnPopulationCleaningStategy(LocalBaseCleaningStrategy):

    def __init__(self, data_to_clean, **kwargs):
        self.bindings = kwargs
        self.data_to_clean = data_to_clean
        self.columns_to_retain = self.bindings['columns_to_retain']
        self.columns_to_rename = self.bindings['columns_to_rename']
        self.translate_values = self.bindings['translate_values']

    def _decode_demo_values(self) -> pd.DataFrame:
        data_to_clean = decode_demo_values(self.data_to_clean, self.translate_values)
        return data_to_clean

    def _filter_columns(self) -> pd.DataFrame:
        data_to_clean = filter_columns(self.data_to_clean, self.columns_to_retain)
        return data_to_clean

    def clean_data(self):
        self.data_to_clean = self._filter_columns()
        self.data_to_clean.rename(columns=self.columns_to_rename, inplace=True)
        self.data_to_clean = self._decode_demo_values()

        return self.data_to_clean


class ItalyPopulationCleaningStategy(LocalBaseCleaningStrategy):

    def __init__(self, data_to_clean, **kwargs):
        self.bindings = kwargs
        self.data_to_clean = data_to_clean
        self.columns_to_retain = self.bindings['columns_to_retain']
        self.columns_to_rename = self.bindings['columns_to_rename']
        self.translate_values = self.bindings['translate_values']

    def _filter_columns(self) -> pd.DataFrame:
        data_to_clean = filter_columns(self.data_to_clean, self.columns_to_retain)
        return data_to_clean

    def _covert_cols_to_rows(self):
        data_to_clean = convert_cols_to_rows(self.data_to_clean,
                                             ItalyPopDataHeaders.TRANSLATE_AGE,
                                             ItalyPopDataHeaders.TRANSLATE_SEX,
                                             ItalyPopDataHeaders.POPULATION)

        return data_to_clean

    def _decode_demo_values(self) -> pd.DataFrame:
        data_to_clean = decode_demo_values(self.data_to_clean, self.translate_values)
        return data_to_clean

    def clean_data(self):
        self.data_to_clean = self._filter_columns()
        self.data_to_clean.rename(columns=self.columns_to_rename, inplace=True)
        self.data_to_clean = self._covert_cols_to_rows()
        self.data_to_clean = self._decode_demo_values()
        drop_total = self.data_to_clean[self.data_to_clean[ItalyPopDataHeaders.TRANSLATE_AGE] == 'Totale'].index
        self.data_to_clean.drop(drop_total, axis=0, inplace=True)
        self.data_to_clean[ItalyPopDataHeaders.TRANSLATE_AGE] = self.data_to_clean[ItalyPopDataHeaders.TRANSLATE_AGE].map(int)
        return self.data_to_clean


class CVDsEuropeCleaningStategy(LocalBaseCleaningStrategy):

    def __init__(self, data_to_clean, **kwargs):
        self.bindings = kwargs
        self.data_to_clean = data_to_clean
        self.columns_to_retain = self.bindings['columns_to_retain']
        self.columns_to_rename = self.bindings['columns_to_rename']
        self.translate_values = self.bindings['translate_values']

    def _filter_columns(self) -> pd.DataFrame:
        data_to_clean = filter_columns(self.data_to_clean, self.columns_to_retain)
        return data_to_clean

    def clean_data(self):
        self.data_to_clean.rename(columns=self.columns_to_rename, inplace=True)
        self.data_to_clean = self._filter_columns()
        self.data_to_clean.dropna(how='any', axis=0, inplace=True)
        return self.data_to_clean


class StandardizedEUPopulationCleaningStrategy(LocalBaseCleaningStrategy):

    def __init__(self, data_to_clean, **kwargs):
        self.bindings = kwargs
        self.data_to_clean = data_to_clean
        self.translate_values = self.bindings['translate_values']
        self.columns_to_rename = self.bindings['columns_to_rename']

    def _decode_demo_values(self) -> pd.DataFrame:
        data_to_clean = decode_demo_values(self.data_to_clean, self.translate_values)
        return data_to_clean

    def clean_data(self):
        self.data_to_clean = self._decode_demo_values()
        self.data_to_clean.rename(columns=self.columns_to_rename, inplace=True)
        self.data_to_clean[StandardPopHeaders.Standardized_Pop] = self.data_to_clean[StandardPopHeaders.Standardized_Pop].map(int)
        return self.data_to_clean
