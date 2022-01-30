from abc import abstractmethod, ABC

import pandas as pd

from code_base.data_cleaners.cleaning_params.cvbg_cleaning_params import CVBGGeneralHeaders as HEADERS
from code_base.data_cleaners.utilities.filter_data import filter_columns


class LocalBaseCleaningStrategy(ABC):

    @abstractmethod
    def clean_data(self):
        pass


class CoronaVirusBGGeneralCleaningStategy(LocalBaseCleaningStrategy):

    def __init__(self, data_to_clean: pd.DataFrame, **kwargs):
        self.bindings = kwargs
        self.data_to_clean = data_to_clean
        self.columns_to_rename = self.bindings['columns_to_rename']
        self.columns_to_retain = self.bindings['columns_to_retain']

    def _filter_columns(self) -> pd.DataFrame:
        data_to_clean = filter_columns(self.data_to_clean, self.columns_to_retain)
        return data_to_clean

    def clean_data(self):
        self.data_to_clean.rename(columns=self.columns_to_rename, inplace=True)
        self.data_to_clean['Date'] = pd.to_datetime(self.data_to_clean['Date'], format='%Y/%m/%d')
        self.data_to_clean[HEADERS.WEEK] = self.data_to_clean['Date'].dt.strftime('%W').map(int) + 1
        self.data_to_clean[HEADERS.YEAR] = self.data_to_clean['Date'].dt.strftime('%Y').map(int)
        self.data_to_clean[HEADERS.YEAR] = self.data_to_clean[HEADERS.YEAR].astype(int)
        self.data_to_clean = self._filter_columns()
        return self.data_to_clean
