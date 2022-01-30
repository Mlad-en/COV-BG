from pathlib import Path
from os import path


class BaseFolderStructure:

    _PROJECT_FOLDER = Path(__file__).parent.parent.parent

    _CODE_BASE_FOLDER = path.join(_PROJECT_FOLDER, 'code_base')

    # Output paths
    DATA_OUTPUT_FOLDER = path.join(_PROJECT_FOLDER, 'data_output')

    EXCESS_MORTALITY = path.join(DATA_OUTPUT_FOLDER, 'Excess Mortality')
    COUNTRIES = path.join(EXCESS_MORTALITY, 'Countries')
    MUNICIPALITIES = path.join(EXCESS_MORTALITY, 'Municipalities')
    REGIONS = path.join(EXCESS_MORTALITY, 'Regions')

    EXCESS_MORTALITY_PREDICTED = path.join(EXCESS_MORTALITY, 'Predicted')
    COUNTRIES_EM = path.join(EXCESS_MORTALITY_PREDICTED, 'Countries')
    MUNICIPALITIES_EM = path.join(EXCESS_MORTALITY_PREDICTED, 'Municipalities')
    REGIONS_EM = path.join(EXCESS_MORTALITY_PREDICTED, 'Regions')

    PYLL = path.join(DATA_OUTPUT_FOLDER, 'PYLL')
    PYLL_COUNTRIES = path.join(PYLL, 'Countries (BG, CZ)')
    PYLL_EU = path.join(PYLL, 'PYLL_EU')

    # Source paths
    DATA_SOURCE_FOLDER = path.join(_PROJECT_FOLDER, 'data_source')
    EU_POPULATION = path.join(DATA_SOURCE_FOLDER, 'Population')
    COVID_MORTALITY = path.join(DATA_SOURCE_FOLDER, 'Covid Mortality')
    COVID_MORTALITY_BULGARIA = path.join(DATA_SOURCE_FOLDER, 'Bulgaria/Combined')
    COVID_MORTALITY_Czechia = path.join(DATA_SOURCE_FOLDER, 'Czechia')
