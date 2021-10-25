from pathlib import Path
from os import path


class BaseFolderStructure:

    _PROJECT_FOLDER = Path(__file__).parent.parent.parent

    _CODE_BASE_FOLDER = path.join(_PROJECT_FOLDER, 'code_base')
    DATA_SOURCE_FOLDER = path.join(_PROJECT_FOLDER, 'data_source')
    DATA_OUTPUT_FOLDER = path.join(_PROJECT_FOLDER, 'data_output')
