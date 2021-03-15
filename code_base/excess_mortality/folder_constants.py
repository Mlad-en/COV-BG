from os import path

from code_base.folder_constants import *

# Source Data
source_excess_mortality = path.join(source_data, 'Excess Mortality')
source_excess_mortality_countries = path.join(source_excess_mortality, 'Countries')
source_excess_mortality_regions = path.join(source_excess_mortality, 'Regions')

# Output Data
output_excess_mortality = path.join(output_data, 'Excess Mortality')
output_excess_mortality_countries = path.join(output_excess_mortality, 'Countries')
output_excess_mortality_regions = path.join(output_excess_mortality, 'Regions')