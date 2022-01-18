import pandas as pd

from code_base.data_bindings.column_naming_consts import COLUMN_HEADING_CONSTS as COL_HEAD
from code_base.data_wrangling.groupings.group_eurostat_data import GroupData


class GroupCVBGGeneralData(GroupData):

    def group_data(self):
        self.df = self.df.groupby([COL_HEAD.YEAR, COL_HEAD.WEEK]).agg({
            'Cases_Last_24_Cases': 'sum',
            'Tests_Last_24_Done': 'sum',
            'Deceased_Last_24_Cases': 'sum',
                                                                       })
        self.df.reset_index(inplace=True)
        return self.df