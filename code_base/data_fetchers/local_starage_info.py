import os

from code_base.data_bindings.data_types import LocalDataSets
from code_base.data_savers.folder_structure import BaseFolderStructure


class LocalDataFetcherInfo:
    """

    """

    AVAILABLE_DATASETS = {
        LocalDataSets.UNDATA_POPULATION,
        LocalDataSets.ITALY_POPULATION,
        LocalDataSets.COVID_MORTALITY_BG,
        LocalDataSets.CVD_EUROPE,
        LocalDataSets.STD_POPULATION_EU,
    }

    FOLDER_LOCATION = {
        LocalDataSets.UNDATA_POPULATION: BaseFolderStructure.EU_POPULATION,
        LocalDataSets.ITALY_POPULATION: BaseFolderStructure.EU_POPULATION,
        LocalDataSets.CVD_EUROPE: BaseFolderStructure.EU_POPULATION,
        LocalDataSets.STD_POPULATION_EU: BaseFolderStructure.EU_POPULATION,
        LocalDataSets.COVID_MORTALITY_BG: BaseFolderStructure.COVID_MORTALITY_BULGARIA,
    }

    FILES = {
        LocalDataSets.UNDATA_POPULATION:
            'UNDATA_Population by age, sex and urban-rural residence_2019.csv',
        LocalDataSets.ITALY_POPULATION:
            'demo.istat - Resident population by age, sex and marital status on 1st January 2020.csv',
        LocalDataSets.CVD_EUROPE: 'Cardiovascular_diseases_Health_update_2021.csv',
        LocalDataSets.STD_POPULATION_EU: 'Standard populations - Federal Health Monitoring.csv',
        LocalDataSets.COVID_MORTALITY_BG:
        'Cov-19_mort_reg.csv'
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
        folder = LocalDataFetcherInfo.FOLDER_LOCATION[self._file_type]
        file = os.path.join(folder, LocalDataFetcherInfo.FILES[self._file_type])
        return file
