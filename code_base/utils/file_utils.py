from datetime import date
from os import path
from typing import List

import pandas as pd

from code_base.excess_mortality.decode_args import FILE_EXT_TYPE


def weeks_for_year(year: int) -> int:
    """
    Per ISO 8601,the last week of the year always contains the 28th of Dec.
    https://en.wikipedia.org/wiki/ISO_week_date#Last_week
    :param year: Year for which last week number is required
    :return: Returns the last week number for a given year (53 weeks or 52 weeks).
    """
    last_week = date(year, 12, 28)
    return last_week.isocalendar()[1]


def generate_past_week_years(start_year: int, end_year: int) -> List:
    """Function is used to generate the
    :param start_year: Start interval for week generation.
    :param end_year: End interval for week generation (inclusive).
    :return: Returns a list of all weeks for the given interval in the format: ['2020W52', '2020W53', '2021W01']
    """
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
    def save_df_to_file(df: pd.DataFrame, location, file_name: str, method: str = 'csv', sheet_name: str ='Sheet1') -> str:
        """

        :param df: DataFrame object that needs to be saved.
        :param location: The output_loc where the DataFrame needs to be saved.
        :param file_name: The file name of the saved file.
        :param method: The file type - by default it's 'csv'. Others are excel, pickle and latex.
        :return: Returns the absolute path to the saved file.
        """

        file_type = FILE_EXT_TYPE.get(method)
        if not file_type:
            raise ValueError('Incorrect Save DF method called.')

        file_name += file_type
        file_path = path.join(location, file_name)

        if method == 'csv':
            df.to_csv(file_path, index=False, encoding='utf-8-sig')
        if method == 'excel':
            df.to_excel(file_path, index=False, encoding='utf-8-sig', sheet_name=sheet_name)
        # TODO: Implement other save df methods
        if method == 'latex':
            raise ValueError('Method NOT yet implemented')
        if method == 'pickle':
            raise ValueError('Method NOT yet implemented')

        return file_path