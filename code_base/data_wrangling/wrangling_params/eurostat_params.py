from code_base.data_bindings.EU_ISO2_translation import EU_COUNTRIES_ISO_2_DECODES
from code_base.data_bindings.EU_NUTS3_translation import EU_DECODE_NUTS3_REGIONS
from code_base.data_wrangling.wrangling_strategies.eurostat_wrangling_strategies import (GroupByAgeSexLocation,
                                                                                         GroupByAgeSexLocationWeek,
                                                                                         GroupBySexLocation,
                                                                                         GroupBySexLocationWeek)


class EurostatParams:
    EXCLUDE_DEFAULT_COUNTRIES = [
        EU_COUNTRIES_ISO_2_DECODES['AD'],
        EU_COUNTRIES_ISO_2_DECODES['AL'],
        EU_COUNTRIES_ISO_2_DECODES['AM'],
        EU_COUNTRIES_ISO_2_DECODES['DE'],
        EU_COUNTRIES_ISO_2_DECODES['GE'],
        EU_COUNTRIES_ISO_2_DECODES['UK'],
    ]

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
        'slw': GroupByAgeSexLocation,
        'asl': GroupBySexLocationWeek,
        'sl': GroupBySexLocation,
    }