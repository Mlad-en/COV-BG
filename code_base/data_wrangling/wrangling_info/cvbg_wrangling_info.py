from code_base.data_bindings.data_types import CoronaVirusBGDataSets
from code_base.data_wrangling.wrangling_strategies import cvbg_wrangling_strategies


class CVBGWranglingConfig:

    WRANGLING_STRATEGIES = {
        CoronaVirusBGDataSets.GENERAL: cvbg_wrangling_strategies.CVBGGeneralWranglingStrategy,
    }


class CVBGWranglingInfo:

    def __init__(self, data_type):
        self._data_type = data_type

    @property
    def wrangling_strategy(self):
        return CVBGWranglingConfig.WRANGLING_STRATEGIES[self._data_type]


if __name__ == '__main__':
    from code_base.data_source.get_source_data import get_source_data
    data = get_source_data(CoronaVirusBGDataSets.GENERAL)
    wrangling = CVBGWranglingInfo(CoronaVirusBGDataSets.GENERAL).wrangling_strategy
    wr = wrangling(2020)
    data = wr.filter_data(data)
    data = wr.group_data(data)
    print(data)
