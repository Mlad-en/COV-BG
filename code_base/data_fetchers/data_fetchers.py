from abc import ABC, abstractmethod
import pandas as pd

from code_base.data_fetchers.eurostat_fetcher_info import EurostatFileInfo


class FetchData(ABC):
    """Class used to fetch data from different sources."""

    @abstractmethod
    def get_data(self) -> pd.DataFrame:
        """Returns a data source as a dataframe object"""
        pass


class FetchEuroStatData(FetchData):

    def __init__(self, eurostat_data_type: str):
        self.file_info = EurostatFileInfo(eurostat_data_type)
        self.csv_params = self.file_info.csv_params
        self.url = self.file_info.file_url

    def get_data(self) -> pd.DataFrame:
        eurostat_df = pd.read_csv(self.url, **self.csv_params)

        return eurostat_df