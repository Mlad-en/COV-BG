from typing import List

from code_base.data_calculations.calc_excess_mortality import CalculateEurostatExcessMortality
from code_base.data_source.get_source_data import get_source_data
from code_base.data_wrangling.wrangle_data import wrangle_excess_mortality_eurostat


def get_excess_mortality_eurostat(data_type,
                                  age_groups: List,
                                  sex_groups: List,
                                  start_week: int,
                                  end_week: int = None,
                                  group_by: str = 'sl',
                                  **additional_params):

    analyze_all_years = additional_params['analyze_years']
    analyze_year = max(analyze_all_years)
    compare_years = [year for year in analyze_all_years if not year == analyze_year]
    clean_data = get_source_data(data_type, **additional_params)
    wrangle_data = wrangle_excess_mortality_eurostat(data_type,
                                                     clean_data,
                                                     analyze_all_years,
                                                     age_groups,
                                                     sex_groups,
                                                     start_week,
                                                     end_week,
                                                     group_by)

    excess_mortality = CalculateEurostatExcessMortality(wrangle_data).calculate_excess_mortality(compare_years,
                                                                                                 analyze_year)

    return excess_mortality


if __name__ == '__main__':
    from code_base.data_bindings.data_types import EurostatDataSets

    years = [2015, 2016, 2017, 2018, 2019, 2020]

    data = get_excess_mortality_eurostat(EurostatDataSets.MORTALITY_BY_SEX_AGE_COUNTRY,
                                         age_groups=['Total'],
                                         sex_groups=['Total'],
                                         start_week=10,
                                         analyze_years=years,
                                         group_by='slw')

