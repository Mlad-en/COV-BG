import os

from code_base.data_bindings.data_types import LocalDataSets
from code_base.data_savers.folder_structure import BaseFolderStructure


class LocalDataFetcherInfo:
    """

    """

    MAIN_FOLDER = BaseFolderStructure.EU_POPULATION

    AVAILABLE_DATASETS = {
        LocalDataSets.UNDATA_Population,
        LocalDataSets.Italy_Population,

    }

    FILES = {
        LocalDataSets.UNDATA_Population:
            'UNDATA_Population by age, sex and urban-rural residence_2019.csv',
        LocalDataSets.Italy_Population:
            'demo.istat - Resident population by age, sex and marital status on 1st January 2020.csv',
    }


class LocalFileInfo:
    """

    """

    def __init__(self, file_type):

        if file_type not in LocalDataFetcherInfo.AVAILABLE_DATASETS:

            data = LocalDataFetcherInfo.AVAILABLE_DATASETS
            raise ValueError(f"File Type not included in the available file types set. Available types are: {data}")

        self._file_type = file_type


    @property
    def file_path(self):
        """
        :return:
        """
        url = LocalDataFetcherInfo.MAIN_FOLDER
        file = os.path.join(url, LocalDataFetcherInfo.FILES[self._file_type])
        return file
