import pandas as pd

from code_base.data_bindings.age_group_translations import AGE_BINDINGS
from code_base.data_bindings.column_naming_consts import COLUMN_HEADING_CONSTS as COL_HEAD
from code_base.data_wrangling.groupings.group_eurostat_data import GroupData


class GroupByAgeSexItalyPopulation(GroupData):

    def group_data(self):
        bins = [0, 4, 9, 14, 19, 24, 29, 34, 39, 44, 49, 54, 59, 64, 69, 74, 79, 84, 89, 150]
        labels = [
            AGE_BINDINGS.AGE_00_04, AGE_BINDINGS.AGE_05_09, AGE_BINDINGS.AGE_10_14, AGE_BINDINGS.AGE_15_19,
            AGE_BINDINGS.AGE_20_24, AGE_BINDINGS.AGE_25_29, AGE_BINDINGS.AGE_30_34, AGE_BINDINGS.AGE_35_39,
            AGE_BINDINGS.AGE_40_44, AGE_BINDINGS.AGE_45_49, AGE_BINDINGS.AGE_50_54, AGE_BINDINGS.AGE_55_59,
            AGE_BINDINGS.AGE_60_64, AGE_BINDINGS.AGE_65_69, AGE_BINDINGS.AGE_70_74, AGE_BINDINGS.AGE_75_79,
            AGE_BINDINGS.AGE_80_84, AGE_BINDINGS.AGE_85_89, AGE_BINDINGS.AGE_GE90,
        ]
        bins = pd.cut(self.df[COL_HEAD.AGE], bins=bins, include_lowest=True, labels=labels)
        self.df = self.df.groupby([bins, COL_HEAD.SEX]).agg({COL_HEAD.POPULATION: 'sum'})
        self.df.reset_index(inplace=True)
        return self.df
