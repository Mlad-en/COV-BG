from os import path
from typing import List, Dict, Optional

import pandas as pd

from code_base.excess_mortality.decode_args import *
from code_base.excess_mortality.utils import *
from url_constants import *

class GetBulkEurostatDataBase:
    def __init__(self, eurostat_data: str, add_current_year: bool = False, current_year_weeks: Optional[int] = None):

        self.eurostat_data: str = eurostat_data

        self.add_current_year: bool = add_current_year
        self.current_year_weeks: Optional[int] = current_year_weeks

        self.split_columns: Dict = {
            'split_from_demo': DECODE_DEMO_COL[self.eurostat_data],
            'split_into_demo': DECODE_DEMO_REPL[self.eurostat_data],
            'split_from_year_week': 'Year_week',
            'split_into_year_week': ['Year', 'Week']
        }
        self.retain_demo_columns = RETAIN_COLUMNS[self.eurostat_data]
        self.replace_location_name = COUNTRY_REPLACE[self.eurostat_data]

        self.eurostat_df: pd.DataFrame = pd.read_csv(self.url, compression='gzip', sep='\t', encoding='utf-8-sig', low_memory=False)

    @property
    def url(self) -> str:
        domain: str = EUROSTAT_DATA['main']
        url_path: str = EUROSTAT_DATA['files'][self.eurostat_data]
        full_url: str = domain + url_path
        return full_url

    @property
    def generate_year_week_columns(self) -> List:
        week_year_columns = generate_past_week_years(2015, 2020)
        if self.add_current_year:
            week_year_columns.extend(generate_current_year_weeks(self.current_year_weeks))
        return week_year_columns

    def split_demographic_data(self, split_from, split_into, separator) -> None:
        col_ind = self.eurostat_df.columns.get_loc(split_from)
        self.eurostat_df[split_into] = self.eurostat_df.iloc[:, col_ind].str.split(separator, expand=True)
        self.eurostat_df.drop(split_from, axis=1, inplace=True)

    def filter_cols(self, year_week_columns):
        filt_columns = self.retain_demo_columns + year_week_columns
        self.eurostat_df.drop(self.eurostat_df.columns[
                                  ~self.eurostat_df.columns.isin(filt_columns)],
                              axis=1,
                              inplace=True)

    def decode_demo_values(self):
        decode_demo_info = {
            'Location': self.replace_location_name,
            'Sex': EUROSTAT_SEX_CONVERSION,
            'Age': EUROSTAT_AGES_CONVERSION
        }
        for key, val in decode_demo_info.items():
            self.eurostat_df[key] = self.eurostat_df.apply(lambda x: val[x[key]], axis=1)

    def save_df(self, file_name: str, loc: str, method: str = 'csv'):

        file_type = FILE_EXT_TYPE.get(method)
        if not file_type:
            raise ValueError('Incorrect Save DF method called.')

        location = loc
        file_name += file_type
        file_path = path.join(location, file_name)

        if method == 'csv':
            self.eurostat_df.to_csv(file_path, index=False, encoding='utf-8-sig')
        # TODO: Implement other save df methods
        if method == 'latex':
            raise ValueError('Method NOT yet implemented')
        if method == 'excel':
            raise ValueError('Method NOT yet implemented')
        if method == 'pickle':
            raise ValueError('Method NOT yet implemented')

        return file_path