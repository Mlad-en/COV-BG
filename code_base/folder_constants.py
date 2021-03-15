from pathlib import Path
from os import path

project_folder = Path(__file__).parent.parent

code = path.join(project_folder, 'code_base')
source_data = path.join(project_folder, 'data_source')
output_data = path.join(project_folder, 'data_output')