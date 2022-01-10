from pathlib import Path
from os import path


class BaseFolderStructure:

    _PROJECT_FOLDER = Path(__file__).parent.parent.parent

    _CODE_BASE_FOLDER = path.join(_PROJECT_FOLDER, 'code_base')

    # Output paths
    DATA_OUTPUT_FOLDER = path.join(_PROJECT_FOLDER, 'data_output')

    _EXCESS_MORTALITY = path.join(DATA_OUTPUT_FOLDER, 'Excess Mortality')
    _COUNTRIES = path.join(_EXCESS_MORTALITY, 'Countries')
    _MUNICIPALITIES = path.join(_EXCESS_MORTALITY, 'Municipalities')
    _REGIONS = path.join(_EXCESS_MORTALITY, 'Regions')

    _EXCESS_MORTALITY_PREDICTED = path.join(_EXCESS_MORTALITY, 'Predicted')
    _COUNTRIES_EM = path.join(_EXCESS_MORTALITY_PREDICTED, 'Countries')
    _MUNICIPALITIES_EM = path.join(_EXCESS_MORTALITY_PREDICTED, 'Municipalities')
    _REGIONS_EM = path.join(_EXCESS_MORTALITY_PREDICTED, 'Regions')

    _PYLL = path.join(DATA_OUTPUT_FOLDER, 'PYLL')
    _PYLL_COUNTRIES = path.join(_PYLL, 'Countries (BG, CZ)')
    _PYLL_EU = path.join(_PYLL, 'PYLL_EU')

    # Source paths
    DATA_SOURCE_FOLDER = path.join(_PROJECT_FOLDER, 'data_source')
    EU_POPULATION = path.join(DATA_SOURCE_FOLDER, 'Population')


    @classmethod
    def get_output_folder_location(cls, file_type, file_sub_type, year):
        """
        
        :param file_type: Options for 
        :param file_sub_type: 
        :param year: 
        :return: 
        """

        locations = {
            # Expected Mortality - Mean Mode
            'e': {
                'r': cls._REGIONS,
                'm': cls._MUNICIPALITIES,
                'c': cls._COUNTRIES,
            },
            # Expected Mortality - Prediction Mode
            'ep': {
                'r': cls._REGIONS_EM,
                'm': cls._MUNICIPALITIES_EM,
                'c': cls._COUNTRIES_EM,
            },
            # PYLL -
            'p': {
                'c': cls._PYLL_COUNTRIES,
                'e': cls._PYLL_EU,
            }
        }
        file_type = locations.get(file_type).get(file_sub_type)

        if file_type:
            year = str(year)
            folder_location = path.join(file_type, year)
            return folder_location