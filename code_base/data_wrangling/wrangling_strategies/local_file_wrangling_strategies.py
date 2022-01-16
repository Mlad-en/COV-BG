import pandas as pd

from code_base.data_bindings.EU_COUNTRIES import UN_LOC_VARS
from code_base.data_bindings.age_group_translations import AGE_BINDINGS, UN_DECODE_AGE_GROUPS
from code_base.data_bindings.column_naming_consts import COLUMN_HEADING_CONSTS
from code_base.data_bindings.sex_translations import UN_DECODE_SEX_GROUPS
from code_base.data_wrangling.filters import filter_specifications
from code_base.data_wrangling.filters.filter_specifications import FilterData
from code_base.data_wrangling.groupings.group_italy_pop import GroupByAgeSexItalyPopulation


class WHOPopulationWranglingStrategy:

    def __init__(self):
        self.age = list(UN_DECODE_AGE_GROUPS.values())
        self.sex = list(UN_DECODE_SEX_GROUPS.values())
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


class ItalyPopulationWranglingStrategy:

    def __init__(self, age, sex):
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
