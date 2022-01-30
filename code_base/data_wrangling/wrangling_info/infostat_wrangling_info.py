from code_base.data_bindings.data_types import InfostatDataSets as DtTp
from code_base.data_wrangling.wrangling_params.infostat_params import InfostatWranglingParams
from code_base.data_wrangling.wrangling_strategies.infostat_wrangling_strategies import \
    PopBySexAgeLocationWranglingStrategy


class InfoWranglingConfig:

    WRANGLING_STRATEGIES = {
        DtTp.POP_BY_SEX_AGE_REG:         PopBySexAgeLocationWranglingStrategy,
        DtTp.AVG_LIFE_EXPECTANCY_BY_SEX: "",
        DtTp.LIFE_EXPECTANCY_BY_SEX:     "",
        DtTp.MORTALITY_BY_SEX_AGE_MUN:   "",
        DtTp.POP_BY_MUNICIPALITY:        "",
    }

    GROUP_BY_DATA = {
        DtTp.POP_BY_SEX_AGE_REG:          InfostatWranglingParams.GROUP_DATA_BY_POPULATION,
        DtTp.AVG_LIFE_EXPECTANCY_BY_SEX:  "",
        DtTp.LIFE_EXPECTANCY_BY_SEX:      "",
        DtTp.MORTALITY_BY_SEX_AGE_MUN:    "",
        DtTp.POP_BY_MUNICIPALITY:         "",
    }

    DEFAULT_EXCLUDE_REGIONS = {
        DtTp.POP_BY_SEX_AGE_REG: ['Total'],
        DtTp.AVG_LIFE_EXPECTANCY_BY_SEX: "",
        DtTp.LIFE_EXPECTANCY_BY_SEX: "",
        DtTp.MORTALITY_BY_SEX_AGE_MUN: "",
        DtTp.POP_BY_MUNICIPALITY: "",
    }


class InfostatWranglingInfo:

    def __init__(self, data_type):
        self._data_type = data_type

    @property
    def wrangling_strategy(self):
        return InfoWranglingConfig.WRANGLING_STRATEGIES[self._data_type]

    @property
    def default_exclude_regions(self):
        return InfoWranglingConfig.DEFAULT_EXCLUDE_REGIONS[self._data_type]

    def group_by_data(self, group_by):
        group_types = InfoWranglingConfig.GROUP_BY_DATA[self._data_type]
        if group_by not in group_types.keys():
            raise ValueError(f'Available data groupings are: {", ".join(group_types.keys())}')

        return group_types[group_by]