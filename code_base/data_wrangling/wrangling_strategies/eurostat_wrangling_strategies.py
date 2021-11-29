from typing import List, Optional

from code_base.data_wrangling.filters.filter_specifications import *
from code_base.data_bindings.column_naming_consts import COLUMN_HEADING_CONSTS as COL_HEAD


class WranglingStrategyBase(ABC):

    @abstractmethod
    def filter_data(self, data: pd.DataFrame) -> pd.DataFrame:
        pass

    @abstractmethod
    def group_data(self, data: pd.DataFrame) -> pd.DataFrame:
        pass


class EurostatExcessMortalityWranglingStrategy(WranglingStrategyBase):

    def __init__(self,
                 age: List,
                 sex: List,
                 location: List,
                 group_by,
                 start_week: int,
                 end_week: Optional[int],
                 years: List[str],):

        self.age = age
        self.sex = sex
        self.location = location
        self.group_by = group_by
        self.start_week = start_week
        self.end_week = end_week
        self.years = years


    @property
    def _full_specs(self) -> List:
        args = [AgeSpecification(self.age),
                SexSpecification(self.sex),
                LocationSpecification(self.location),
                WeekStartSpecification(self.start_week),
                WeekEndSpecification(self.end_week)]

        return args

    @property
    def _no_end_week_specs(self) -> List:
        args = [AgeSpecification(self.age),
                SexSpecification(self.sex),
                LocationSpecification(self.location),
                WeekStartSpecification(self.start_week)]

        return args

    @property
    def _specifications(self) -> Specification:
        if self.end_week:
            args = self._full_specs
            return AndSpecification(*args)

        args = self._no_end_week_specs
        return AndSpecification(*args)

    def filter_data(self, data: pd.DataFrame) -> pd.DataFrame:
        data[COL_HEAD.WEEK] = data.loc[:, COL_HEAD.WEEK].astype(int, errors='raise')
        data = FilterData(self._specifications).filter_out_data(data)
        data[self.years] = data.loc[:, self.years].astype('float64', errors='ignore')
        return data

    def group_data(self, data: pd.DataFrame) -> pd.DataFrame:
        data = self.group_by(data).group_data()
        return data


class EurostatEUPopulationWranglingStrategy(WranglingStrategyBase):

    def __init__(self, age: List, sex: List, group_by):
        self.age = age
        self.sex = sex
        self.group_by = group_by

    @property
    def _full_specs(self) -> List:
        args = [AgeSpecification(self.age),
                SexSpecification(self.sex)]

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
