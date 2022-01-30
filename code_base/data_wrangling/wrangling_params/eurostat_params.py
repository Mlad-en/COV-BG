from code_base.data_bindings.EU_ISO2_translation import EU_COUNTRIES_ISO_2_DECODES
from code_base.data_bindings.EU_NUTS3_translation import EU_DECODE_NUTS3_REGIONS
from code_base.data_wrangling.groupings.group_eurostat_data import (GroupByAgeSexLocationWeek,
                                                                    GroupByAgeSexLocation,
                                                                    GroupBySexLocationWeek,
                                                                    GroupBySexLocation)


class EurostatParams:

    """
    Excluding countries that do not have complete information for the past 5 years (e.g. no mortality statistics for
    Germany for 2015) or incomplete information for the years analyzed (No Eurostat info for UK for the last week of 2020
    and no info for the entire of 2021.
    """
    EXCLUDE_DEFAULT_COUNTRIES = [
        EU_COUNTRIES_ISO_2_DECODES['AD'],
        EU_COUNTRIES_ISO_2_DECODES['AL'],
        EU_COUNTRIES_ISO_2_DECODES['AM'],
        EU_COUNTRIES_ISO_2_DECODES['DE'],
        EU_COUNTRIES_ISO_2_DECODES['GE'],
        EU_COUNTRIES_ISO_2_DECODES['UK'],
    ]
    """
    Excluding Bulgarian regions based on their NUTS status. Only NUTS-3 regions are used for this analysis. 
    NUTS-2 regions are thus to be exluced.
    """
    EXCLUDE_DEFAULT_REGIONS = [
        EU_DECODE_NUTS3_REGIONS['BG'],
        EU_DECODE_NUTS3_REGIONS['BG3'],
        EU_DECODE_NUTS3_REGIONS['BG31'],
        EU_DECODE_NUTS3_REGIONS['BG32'],
        EU_DECODE_NUTS3_REGIONS['BG33'],
        EU_DECODE_NUTS3_REGIONS['BG34'],
        EU_DECODE_NUTS3_REGIONS['BG4'],
        EU_DECODE_NUTS3_REGIONS['BG41'],
        EU_DECODE_NUTS3_REGIONS['BG42'],
    ]

    GROUP_DATA_BY_MORTALITY = {
        'all': GroupByAgeSexLocationWeek,
        'asl': GroupByAgeSexLocation,
        'slw': GroupBySexLocationWeek,
        'sl': GroupBySexLocation,
    }

    GROUP_DATA_BY_POPULATION = {
        'asl': GroupByAgeSexLocation,
        'sl': GroupBySexLocation
    }