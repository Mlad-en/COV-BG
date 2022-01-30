from code_base.data_bindings import data_types
from code_base.data_fetchers import data_fetchers


def fetch_data(data_type, data_type_class, **kwargs):
    mapping = {
        data_types.EurostatDataSets: data_fetchers.FetchEuroStatData,
        data_types.WHODataSets: data_fetchers.FetchWHOData,
        data_types.LocalDataSets: data_fetchers.FetchLocalData,
    }
    fetcher = mapping[data_type_class](data_type)
    data = fetcher.get_data()
    return data
