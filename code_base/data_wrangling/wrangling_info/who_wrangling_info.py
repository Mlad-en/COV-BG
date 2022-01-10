from code_base.data_bindings.data_types import WHODataSets
from code_base.data_wrangling.wrangling_strategies.who_wrangling_strategies import WHOLifeExpectancyWranglingStrategy


class WhoWranglingConfig:

    WRANGLING_STRATEGIES = {
        WHODataSets.LIFE_EXPECTANCY_BY_AGE_SEX: WHOLifeExpectancyWranglingStrategy,
    }


class WhoWranglingInfo:

    def __init__(self, data_type):
        self._data_type = data_type

    @property
    def wrangling_strategy(self):
        return WhoWranglingConfig.WRANGLING_STRATEGIES[self._data_type]