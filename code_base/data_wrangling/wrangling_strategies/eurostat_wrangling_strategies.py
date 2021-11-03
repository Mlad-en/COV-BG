from abc import ABC, abstractmethod
from typing import List

from code_base.data_wrangling.filters.filter_specifications import *
from code_base.data_bindings.column_naming_consts import COLUMN_HEADING_CONSTS as COL_HEAD


class GroupData(ABC):

    def __init__(self, df: pd.DataFrame):
        self.df = df

    @abstractmethod
    def group_data(self):
        pass


class GroupByAgeSexLocationWeek(GroupData):

    def group_data(self):
        self.df.fillna(method='pad', axis=1, inplace=True)
        return self.df.groupby([COL_HEAD.AGE, COL_HEAD.SEX, COL_HEAD.LOCATION, COL_HEAD.WEEK], as_index=False).sum()


class GroupByAgeSexLocation(GroupData):

    def group_data(self):
        self.df.drop([COL_HEAD.WEEK], axis=1, inplace=True)
        return self.df.groupby([COL_HEAD.AGE, COL_HEAD.SEX, COL_HEAD.LOCATION], as_index=False).sum()


class GroupBySexLocationWeek(GroupData):

    def group_data(self):
        self.df.fillna(method='pad', inplace=True)
        self.df.drop([COL_HEAD.AGE], axis=1, inplace=True)
        return self.df.groupby([COL_HEAD.SEX, COL_HEAD.LOCATION, COL_HEAD.WEEK], as_index=False).sum()


class GroupBySexLocation(GroupData):

    def group_data(self):
        self.df.drop([COL_HEAD.AGE, COL_HEAD.WEEK], axis=1, inplace=True)
        return self.df.groupby([COL_HEAD.SEX, COL_HEAD.LOCATION], as_index=False).sum()


class WranglingStrategyBase(ABC):

    @abstractmethod
    def prepare_data(self) -> pd.DataFrame:
        pass


class EurostatExcessMortalityWranglingStrategy(WranglingStrategyBase):

    def __init__(self,
                 data: pd.DataFrame,
                 age: List,
                 sex: List,
                 location: List,
                 group_by,
                 start_week: int,
                 end_week: int,
                 years: List[str],):

        self.data = data
        self.age = age
        self.sex = sex
        self.location = location
        self.group_by = group_by
        self.start_week = start_week
        self.end_week = end_week
        self.years = years

    @property
    def _specifications(self) -> Specification:
        args = [AgeSpecification(self.age),
                SexSpecification(self.sex),
                LocationSpecification(self.location),
                WeekStartSpecification(self.start_week)]
        if self.end_week:
            args.append(AgeSpecification(self.age))

        return AndSpecification(*args)

    def prepare_data(self) -> pd.DataFrame:
        self.data[COL_HEAD.WEEK] = self.data.loc[:, COL_HEAD.WEEK].astype(int, errors='raise')
        wrangled_data = FilterData(self._specifications).filter_out_data(self.data)
        wrangled_data[self.years] = wrangled_data.loc[:, self.years].astype('float64', errors='ignore')
        wrangled_data = self.group_by(wrangled_data).group_data()
        return wrangled_data


class EurostatEUPopulationWranglingStrategy(WranglingStrategyBase):

    def prepare_data(self) -> pd.DataFrame:
        pass
