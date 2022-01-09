from code_base.data_bindings.data_types import EurostatDataSets, WHODataSets
from code_base.data_fetchers.data_fetchers import FetchEuroStatData, FetchWHOData


# TODO: Add handling if dynamic fetch fails
def fetch_data(data_type, data_type_class, **kwargs):
    mapping = {
        EurostatDataSets: FetchEuroStatData,
        WHODataSets: FetchWHOData,
    }
    fetcher = mapping[data_type_class](data_type)
    data = fetcher.get_data()
    return data
