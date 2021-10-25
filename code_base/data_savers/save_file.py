from os import path
from typing import Dict

import pandas as pd

from code_base.data_savers.file_extensions import FILE_EXT_TYPE


class SaveFile:
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