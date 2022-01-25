from abc import ABC, abstractmethod

import pandas as pd

from code_base.data_bindings.column_naming_consts import COLUMN_HEADING_CONSTS as COL_HEAD


class GroupData(ABC):

    def __init__(self, df: pd.DataFrame):
        self.df = df

    @abstractmethod
    def group_data(self):
        pass


class GroupByAgeSex(GroupData):

    def group_data(self):
        return self.df.groupby([COL_HEAD.AGE, COL_HEAD.SEX], as_index=False).sum()
