from os import path
from typing import Dict, List

import pandas as pd

from code_base.data_savers.file_extensions import FILE_EXT_TYPE


class NameFile:

    @staticmethod
    def generate_name(args):
        name = '_'.join([str(el) for el in args])

        return name

    @staticmethod
    def get_age_els(age_groups: List):
        if len(age_groups) == 1 and age_groups[0] == 'Total':
            return 'Total'
        if len(age_groups) == 1:
            return age_groups[0]
        if len(age_groups) > 1:
            first_el = age_groups[0].split('-')[0]
            second_el = age_groups[-1].split('-')[1]
            return first_el + '-' + second_el


class SaveFile:

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

    @staticmethod
    def prep_multisheet_xlsx(df: pd.DataFrame, split_df_on_column: str) -> Dict[str, pd.DataFrame]:

        col_on = df[split_df_on_column].unique()
        dfs = {}
        for col_val in col_on:
            dfs[col_val] = df[df[split_df_on_column] == col_val].copy()

        return dfs