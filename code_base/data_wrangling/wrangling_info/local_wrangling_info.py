from code_base.data_bindings.data_types import LocalDataSets
from code_base.data_wrangling.wrangling_strategies import local_file_wrangling_strategies


class LocalStorageWranglingConfig:

    WRANGLING_STRATEGIES = {
        LocalDataSets.UNDATA_POPULATION: local_file_wrangling_strategies.WHOPopulationWranglingStrategy,
        LocalDataSets.ITALY_POPULATION: local_file_wrangling_strategies.ItalyPopulationWranglingStrategy,
        LocalDataSets.STD_POPULATION_EU: local_file_wrangling_strategies.StandardEuPopulationWranglingStrategy

    }


class LocalStorageWranglingInfo:

    def __init__(self, data_type):
        self._data_type = data_type

    @property
    def wrangling_strategy(self):
        return LocalStorageWranglingConfig.WRANGLING_STRATEGIES[self._data_type]
