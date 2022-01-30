from abc import ABC, abstractmethod

import pandas as pd

from code_base.data_cleaners.utilities.filter_data import filter_columns
from code_base.data_cleaners.utilities.translate_values import decode_demo_values


class WHOBaseCleaningStrategy(ABC):

    @abstractmethod
    def clean_data(self):
        pass


class WHoLifeExpectancyCleaningStrategy(WHOBaseCleaningStrategy):

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

    def clean_data(self) -> pd.DataFrame:
        self.data_to_clean = self._filter_columns()
        self.data_to_clean.rename(columns=self.columns_to_rename, inplace=True)
        self.data_to_clean = self._decode_demo_values()
        self.data_to_clean = self.data_to_clean.dropna(how='any')

        return self.data_to_clean