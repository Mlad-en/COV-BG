from abc import ABC, abstractmethod
from io import StringIO
from typing import Optional

import pandas as pd
import requests

from code_base.data_bindings.data_types import WHODataSets
from code_base.data_fetchers.eurostat_fetcher_info import EurostatFileInfo
from code_base.data_fetchers.who_fetcher_info import WHOIntFileInfo


class FetchData(ABC):
    """Class used to fetch data from different sources."""

    @abstractmethod
    def get_data(self) -> pd.DataFrame:
        """Returns a data source as a dataframe object"""
        pass


class FetchEuroStatData(FetchData):

    def __init__(self, eurostat_data_type):
        self.file_info = EurostatFileInfo(eurostat_data_type)
        self.csv_params = self.file_info.csv_params
        self.url = self.file_info.file_url

    def get_data(self) -> pd.DataFrame:
        eurostat_df = pd.read_csv(self.url, **self.csv_params)

        return eurostat_df


class FetchWHOIntData(FetchData):

    def __init__(self, whoint_data_type: WHODataSets, year: Optional[str] = None):
        self.file_info = WHOIntFileInfo(whoint_data_type)
        self.url = self.file_info.file_url
        self.year = year if year else '2019'

    def get_data(self) -> pd.DataFrame:
        self.url = self.url.replace('###YEAR###', self.year)

        req = requests.get(self.url)
        data = StringIO(req.text)
        df = pd.read_csv(data, encoding='utf-8-sig')

        return df
