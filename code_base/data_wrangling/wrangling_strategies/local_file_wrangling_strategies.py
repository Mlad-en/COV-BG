from typing import List

import pandas as pd

from code_base.data_bindings.EU_COUNTRIES import UN_LOC_VARS
from code_base.data_bindings.age_group_translations import AGE_BINDINGS
from code_base.data_wrangling.filters import filter_specifications
from code_base.data_wrangling.filters.filter_specifications import FilterData
from code_base.data_wrangling.groupings.group_eurostat_data import GroupByAgeSexLocation
from code_base.data_wrangling.groupings.group_italy_pop import GroupByAgeSexItalyPopulation
from code_base.data_wrangling.groupings.group_std_pop import GroupByAgeSex


class WHOPopulationWranglingStrategy:

    def __init__(self, sexes: List[str]):
        self.age = [AGE_BINDINGS.AGE_85_89, AGE_BINDINGS.AGE_GE90]
        self.sex = sexes
        self.location = UN_LOC_VARS
        self.area = ['Urban', 'Rural']

    @property
    def _specifications(self) -> filter_specifications.Specification:
        args = [
            filter_specifications.AgeSpecification(self.age),
            filter_specifications.SexSpecification(self.sex),
            filter_specifications.AreaSpecification(self.area),
            filter_specifications.LocationIncludeSpecification(self.location)
        ]

        return filter_specifications.AndSpecification(*args)

    def filter_data(self, data: pd.DataFrame) -> pd.DataFrame:
        data = filter_specifications.FilterData(self._specifications).filter_out_data(data)

        return data

    def group_data(self, data: pd.DataFrame) -> pd.DataFrame:
        data = GroupByAgeSexLocation(data).group_data()
        return data


class ItalyPopulationWranglingStrategy:

    def __init__(self, age: List[str], sex: List[str]):
        self.age = age
        self.sex = sex

    @property
    def _specifications(self) -> filter_specifications.Specification:
        args = [
            filter_specifications.AgeSpecification(self.age),
            filter_specifications.SexSpecification(self.sex),
        ]

        return filter_specifications.AndSpecification(*args)

    def filter_data(self, data: pd.DataFrame) -> pd.DataFrame:
        data = FilterData(self._specifications).filter_out_data(data)
        return data

    def group_data(self, data: pd.DataFrame) -> pd.DataFrame:
        data = GroupByAgeSexItalyPopulation(data).group_data()
        return data


class StandardEuPopulationWranglingStrategy:

    def __init__(self, sex: List[str]):
        self.sex = sex

    @property
    def _specifications(self) -> filter_specifications.Specification:
        args = [
            filter_specifications.SexSpecification(self.sex),
        ]

        return filter_specifications.AndSpecification(*args)

    def filter_data(self, data: pd.DataFrame) -> pd.DataFrame:
        data = FilterData(self._specifications).filter_out_data(data)
        return data

    def group_data(self, data: pd.DataFrame) -> pd.DataFrame:
        data = GroupByAgeSex(data).group_data()
        return data
