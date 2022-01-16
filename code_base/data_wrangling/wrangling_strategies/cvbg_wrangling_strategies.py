import pandas as pd

from code_base.data_wrangling.filters import filter_specifications
from code_base.data_wrangling.filters.filter_specifications import FilterData
from code_base.data_wrangling.groupings.group_italy_pop import GroupByAgeSexItalyPopulation


class CVBGGeneralWranglingStrategy:

    def __init__(self, year):
        self.year = year

    @property
    def _specifications(self) -> filter_specifications.Specification:
        args = [
            filter_specifications.YearSpecification(self.year),
        ]

        return filter_specifications.AndSpecification(*args)

    def filter_data(self, data: pd.DataFrame) -> pd.DataFrame:
        data = FilterData(self._specifications).filter_out_data(data)
        return data

    def group_data(self, data: pd.DataFrame) -> pd.DataFrame:
        data = GroupByAgeSexItalyPopulation(data).group_data()
        return data
