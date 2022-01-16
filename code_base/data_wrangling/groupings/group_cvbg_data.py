import pandas as pd

from code_base.data_bindings.column_naming_consts import COLUMN_HEADING_CONSTS as COL_HEAD
from code_base.data_wrangling.groupings.group_eurostat_data import GroupData


class GroupByAgeSexItalyPopulation(GroupData):

    def group_data(self):
        self.df = self.df.groupby([bins, COL_HEAD.SEX]).agg({COL_HEAD.POPULATION: 'sum'})
        self.df.reset_index(inplace=True)
        return self.df
