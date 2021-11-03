from typing import List

import pandas as pd

from code_base.data_wrangling.wrangling_info.eurostat_wrangling_info import EurostatWranglingInfo


def wrangle_excess_mortality_eurostat(data_type: str,
                                      data_source: pd.DataFrame,
                                      analyze_years: List[str],
                                      age_groups: List,
                                      sex_groups: List,
                                      start_week: int,
                                      end_week: int = None,
                                      group_by: str = 'sl'):

    data_wrangling_info = EurostatWranglingInfo(data_type)
    wrangling_strategy = data_wrangling_info.wrangling_strategy
    exclude_locations = data_wrangling_info.default_exclude_regions
    grouping = data_wrangling_info.group_by_data(group_by)

    data_source = data_source
    filtered_data = wrangling_strategy(data=data_source,
                                       age=age_groups,
                                       sex=sex_groups,
                                       location=exclude_locations,
                                       group_by=grouping,
                                       start_week=start_week,
                                       end_week=end_week,
                                       years=analyze_years).prepare_data()

    return filtered_data
