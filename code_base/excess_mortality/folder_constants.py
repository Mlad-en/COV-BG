from code_base.utils.folder_constants import *

# Source Data
source_excess_mortality = path.join(source_data, 'Excess Mortality')
source_excess_mortality_countries = path.join(source_excess_mortality, 'Countries')
source_excess_mortality_regions = path.join(source_excess_mortality, 'Regions')

source_eu_population = path.join(source_data, 'Population')
source_infostat_raw = path.join(source_data, 'InfoStat - Download BIN')
source_infostat_cleaned = path.join(source_data, 'InfoStat - Cleaned')

source_cov_mort = path.join(source_data, 'Covid Mortality')
source_cov_mort_cz = path.join(source_cov_mort, 'Czechia')
source_cov_mort_bg = path.join(source_cov_mort, 'Bulgaria')
source_cov_bg_auto = path.join(source_cov_mort_bg, 'Automated')
source_cov_bg_comb = path.join(source_cov_mort_bg, 'Combined')


# Output Data
output_excess_mortality = path.join(output_data, 'Excess Mortality')
output_excess_mortality_countries = path.join(output_excess_mortality, 'Countries')
output_excess_mortality_regions = path.join(output_excess_mortality, 'Regions')
