from typing import List

from code_base.data_calculations.calc_excess_mortality import CalculateEurostatExcessMortality
from code_base.data_source.get_source_data import get_source_data
from code_base.data_wrangling.wrangling_info.eurostat_wrangling_info import EurostatWranglingInfo


def get_excess_mortality_eurostat(data_type,
                                  age_groups: List,
                                  sex_groups: List,
                                  start_week: int,
                                  end_week: int = None,
                                  group_by: str = 'sl',
                                  **additional_params):

    clean_data = get_source_data(data_type, **additional_params)

    analyze_all_years = additional_params['analyze_years']
    analyze_year = max(analyze_all_years)
    compare_years = [year for year in analyze_all_years if not year == analyze_year]

    data_wrangling_info = EurostatWranglingInfo(data_type)
    exclude_locations = data_wrangling_info.default_exclude_regions
    grouping = data_wrangling_info.group_by_data(group_by)
    wrangling_strategy = data_wrangling_info.wrangling_strategy(age=age_groups,
                                                                sex=sex_groups,
                                                                location=exclude_locations,
                                                                group_by=grouping,
                                                                start_week=start_week,
                                                                end_week=end_week,
                                                                years=analyze_all_years)

    wranged_data = wrangling_strategy.filter_data(clean_data)
    excess_mort_calcs = CalculateEurostatExcessMortality(wranged_data)
    excess_mort_calcs.add_mean_mort(compare_years)
    wranged_data = excess_mort_calcs.df
    excess_mort_calcs.df = wrangling_strategy.group_data(wranged_data)
    wranged_data = excess_mort_calcs.calculate_excess_mortality(compare_years, analyze_year)

    return wranged_data