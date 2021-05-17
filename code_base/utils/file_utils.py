from datetime import date
from os import path
from typing import List, Dict

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
    :return: Returns a list of all weeks for the given interval in the format: ['2020W52 ', '2020W53 ', '2021W01 ']
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


def clean_unneeded_symbols(df: pd.DataFrame, symbol_to_replace: str, replace_with: str) -> pd.DataFrame:
    return df.replace(symbol_to_replace, replace_with, regex=True)


class SaveFileMixin:
    def __init__(self):
        pass

    @staticmethod
    def generate_file_path(location: str, file_name: str, method: str) -> str:
        """
        Method generates an absolute file path.
        :param location: Location of the file that is to be generated.
        :param file_name: The name of the file to be created.
        :param method: The type of application that needs to be reading this file - e.g. csv, excel. This will return the
        appropriate application extension.
        :return: Returns an absolute file path string.
        """
        file_type = FILE_EXT_TYPE.get(method)
        if not file_type:
            raise ValueError('Incorrect Save DF method called.')

        file_name += file_type
        file_path = path.join(location, file_name)

        return file_path

    def save_df_to_file(self,
                        df: pd.DataFrame,
                        location: str,
                        file_name: str,
                        method: str = 'csv',
                        sheet_name: str = 'Sheet1') -> str:
        """

        :param df: DataFrame object that needs to be saved.
        :param location: The output_loc where the DataFrame needs to be saved.
        :param file_name: The file name of the saved file.
        :param sheet_name: Default sheetname for files.
        :param method: The file type - by default it's 'csv'. Others are excel, pickle and latex.
        :return: Returns the absolute path to the saved file.
        """

        file_path = self.generate_file_path(location=location, file_name=file_name, method=method)

        if method == 'csv':
            df.to_csv(file_path, index=False, encoding='utf-8-sig')
        if method == 'excel':
            df.to_excel(file_path, sheet_name=sheet_name, index=False, encoding='utf-8-sig')

        return file_path

    def save_multisheet_xlsx(self,
                             dfs: Dict[str, pd.DataFrame],
                             location: str,
                             file_name: str) -> str:
        """

        :param dfs:
        :param location:
        :param file_name:
        :return:
        """
        file_path = self.generate_file_path(location=location, file_name=file_name, method='excel')

        with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
            for sheet_name, datafrm in dfs.items():
                datafrm.to_excel(writer, sheet_name=sheet_name, index=False, encoding='utf-8-sig')

        return file_path