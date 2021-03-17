from datetime import date
from os import path
from typing import List

import pandas as pd

from code_base.excess_mortality.decode_args import FILE_EXT_TYPE


def weeks_for_year(year: int) -> int:
    # per ISO 8601,the last week of the year always contains the 28th of Dec.
    # https://en.wikipedia.org/wiki/ISO_week_date#Last_week
    last_week = date(year, 12, 28)
    return last_week.isocalendar()[1]


def generate_past_week_years(start_year: int, end_year: int) -> List:
    week_year = []
    years = [year for year in range(start_year, end_year+1)]
    [[week_year.append(f'{year}W{str(week).zfill(2)} ') for week in range(1, weeks_for_year(year)+1)] for year in years]
    return week_year


def generate_current_year_weeks(num_weeks: int) -> List:
    curr_year = []
    year = date.today().year
    [curr_year.append(f'{year}W{str(week).zfill(2)} ') for week in range(1, num_weeks+1)]
    return curr_year


def get_years_to_compare(df_year, compare_years):
    if compare_years:
        return compare_years
    else:
        start_range = df_year - 5
        end_range = df_year - 1
        return [start_range, end_range]


def clean_unneeded_symbols(df: pd.DataFrame, symbol_to_replace: str, replace_with: str) -> pd.DataFrame:
    return df.replace(symbol_to_replace, replace_with, regex=True)


class SaveFile:
    def __init__(self):
        pass

    @staticmethod
    def save_df(df: pd.DataFrame, location, file_name: str, method: str = 'csv') -> str:

        file_type = FILE_EXT_TYPE.get(method)
        if not file_type:
            raise ValueError('Incorrect Save DF method called.')

        file_name += file_type
        file_path = path.join(location, file_name)

        if method == 'csv':
            df.to_csv(file_path, index=False, encoding='utf-8-sig')
        # TODO: Implement other save df methods
        if method == 'latex':
            raise ValueError('Method NOT yet implemented')
        if method == 'excel':
            raise ValueError('Method NOT yet implemented')
        if method == 'pickle':
            raise ValueError('Method NOT yet implemented')

        return file_path