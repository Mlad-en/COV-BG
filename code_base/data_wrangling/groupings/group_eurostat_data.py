from abc import ABC, abstractmethod

import pandas as pd

from code_base.data_bindings.column_naming_consts import COLUMN_HEADING_CONSTS as COL_HEAD


class GroupData(ABC):

    def __init__(self, df: pd.DataFrame):
        self.df = df

    @abstractmethod
    def group_data(self):
        pass


class GroupByAgeSexLocationWeek(GroupData):

    def group_data(self):
        self.df.fillna(method='pad', inplace=True)
        return self.df.groupby([COL_HEAD.AGE, COL_HEAD.SEX, COL_HEAD.LOCATION, COL_HEAD.WEEK], as_index=False).sum()


class GroupByAgeSexLocation(GroupData):

    def group_data(self):
        self.df.drop([COL_HEAD.WEEK], axis=1, inplace=True, errors='ignore')
        return self.df.groupby([COL_HEAD.AGE, COL_HEAD.SEX, COL_HEAD.LOCATION], as_index=False).sum()


class GroupBySexLocationWeek(GroupData):

    def group_data(self):
        self.df.fillna(method='pad', inplace=True)
        self.df.drop([COL_HEAD.AGE], axis=1, inplace=True)
        return self.df.groupby([COL_HEAD.SEX, COL_HEAD.LOCATION, COL_HEAD.WEEK], as_index=False).sum()


class GroupBySexLocation(GroupData):

    def group_data(self):
        self.df.drop([COL_HEAD.AGE, COL_HEAD.WEEK], axis=1, inplace=True, errors='ignore')
        return self.df.groupby([COL_HEAD.SEX, COL_HEAD.LOCATION], as_index=False).sum()
