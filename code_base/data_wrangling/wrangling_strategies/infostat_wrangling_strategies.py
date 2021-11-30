from abc import ABC, abstractmethod
from typing import List

import pandas as pd

from code_base.data_bindings.column_naming_consts import COLUMN_HEADING_CONSTS as COL_HEAD
from code_base.data_wrangling.filters.filter_specifications import (AgeSpecification,
                                                                    SexSpecification,
                                                                    LocationSpecification,
                                                                    Specification,
                                                                    AndSpecification,
                                                                    FilterData)


class WranglingStrategyBase(ABC):

    @abstractmethod
    def filter_data(self, data: pd.DataFrame) -> pd.DataFrame:
        pass

    @abstractmethod
    def group_data(self, data: pd.DataFrame) -> pd.DataFrame:
        pass


class PopBySexAgeLocationWranglingStrategy(WranglingStrategyBase):

    def __init__(self, age: List, sex: List, location: List, group_by):
        self.age = age
        self.sex = sex
        self.location = location
        self.group_by = group_by

    @property
    def _full_specs(self) -> List:
        args = [AgeSpecification(self.age),
                SexSpecification(self.sex),
                LocationSpecification(self.location)]

        return args

    @property
    def _specifications(self) -> Specification:
        args = self._full_specs
        return AndSpecification(*args)

    def filter_data(self, data: pd.DataFrame) -> pd.DataFrame:
        data[COL_HEAD.POPULATION] = data[COL_HEAD.POPULATION].astype(int, errors='raise')
        data = FilterData(self._specifications).filter_out_data(data)
        return data

    def group_data(self, data: pd.DataFrame) -> pd.DataFrame:
        data = self.group_by(data).group_data()
        return data
