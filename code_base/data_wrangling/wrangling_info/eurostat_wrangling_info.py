from code_base.data_bindings.data_types import EurostatDataSets as DtTp
from code_base.data_wrangling.wrangling_params.eurostat_params import EurostatParams
from code_base.data_wrangling.wrangling_strategies.eurostat_wrangling_strategies import *


class EurostatWranglingConfig:

    WRANGLING_STRATEGIES = {
        DtTp.MORTALITY_BY_SEX_AGE_COUNTRY: EurostatExcessMortalityWranglingStrategy,
        DtTp.MORTALITY_BY_SEX_AGE_REGION:  EurostatExcessMortalityWranglingStrategy,
        DtTp.POP_BY_SEX_AGE_COUNTRY:       EurostatEUPopulationWranglingStrategy,
    }

    DEFAULT_EXCLUDE_REGIONS = {
        DtTp.MORTALITY_BY_SEX_AGE_COUNTRY: EurostatParams.EXCLUDE_DEFAULT_COUNTRIES,
        DtTp.MORTALITY_BY_SEX_AGE_REGION:  EurostatParams.EXCLUDE_DEFAULT_REGIONS,
        DtTp.POP_BY_SEX_AGE_COUNTRY:       EurostatParams.EXCLUDE_DEFAULT_COUNTRIES,
    }

    GROUP_BY_DATA = {
        DtTp.MORTALITY_BY_SEX_AGE_COUNTRY: EurostatParams.GROUP_DATA_BY_MORTALITY,
        DtTp.MORTALITY_BY_SEX_AGE_REGION:  EurostatParams.GROUP_DATA_BY_MORTALITY,
        DtTp.POP_BY_SEX_AGE_COUNTRY:       EurostatParams.GROUP_DATA_BY_POPULATION,
    }


class EurostatWranglingInfo:

    def __init__(self, data_type):
        self._data_type = data_type

    @property
    def wrangling_strategy(self):
        return EurostatWranglingConfig.WRANGLING_STRATEGIES[self._data_type]

    # TODO: add ability to exclude non-default regions from analysis.
    @property
    def default_exclude_regions(self):
        return EurostatWranglingConfig.DEFAULT_EXCLUDE_REGIONS[self._data_type]

    def group_by_data(self, group_by):
        group_types = EurostatWranglingConfig.GROUP_BY_DATA[self._data_type]
        if group_by not in group_types.keys():
            raise ValueError(f'Available data groupings are: {", ".join(group_types.keys())}')

        return group_types[group_by]
