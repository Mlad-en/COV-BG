from code_base.utils.folder_constants import *

# Source Data
source_life_data = path.join(source_data, 'Life Expectancies')
source_WHO_life_data = path.join(source_life_data, 'WHO Life Tables')
source_le_countries_data = path.join(source_life_data, 'Countries (BG, CZ)')

# Output Data
output_pyll = path.join(output_data, 'PYLL')
output_pyll_eu = path.join(output_pyll, 'PYLL_EU')
output_pyll_cntr = path.join(output_pyll, 'Countries (BG, CZ)')
output_pyll_bg = path.join(output_pyll_cntr, 'Bulgaria')
output_pyll_cz = path.join(output_pyll_cntr, 'Czechia')