from abc import ABC, abstractmethod
from io import StringIO
from typing import Optional

import pandas as pd
import requests

from code_base.data_bindings.data_types import WHODataSets
from code_base.data_fetchers.eurostat_fetcher_info import EurostatFileInfo
from code_base.data_fetchers.who_fetcher_info import WHOFileInfo


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


class FetchWHOData(FetchData):

    def __init__(self, whoint_data_type: WHODataSets):
        """

        :param whoint_data_type: The type of file to be requested from the World Health Organization.
        """
        self.file_info = WHOFileInfo(whoint_data_type)
        self.url = self.file_info.file_url

    def get_data(self) -> pd.DataFrame:
        req = requests.get(self.url)
        data = StringIO(req.text)
        df = pd.read_csv(data, encoding='utf-8-sig')

        return df
