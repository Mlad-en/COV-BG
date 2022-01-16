from code_base.data_bindings.data_types import CoronaVirusBGDataSets
from code_base.data_wrangling.wrangling_strategies import cvbg_wrangling_strategies


class WhoWranglingConfig:

    WRANGLING_STRATEGIES = {
        CoronaVirusBGDataSets.GENERAL: cvbg_wrangling_strategies.CVBGGeneralWranglingStrategy,
    }


class WhoWranglingInfo:

    def __init__(self, data_type):
        self._data_type = data_type

    @property
    def wrangling_strategy(self):
        return WhoWranglingConfig.WRANGLING_STRATEGIES[self._data_type]


if __name__ == '__main__':
    from code_base.data_source.get_source_data import get_source_data
    data = get_source_data(CoronaVirusBGDataSets.GENERAL)
    wrangling = WhoWranglingInfo(CoronaVirusBGDataSets.GENERAL).wrangling_strategy

    print(wrangling(2020).filter_data(data).columns)
