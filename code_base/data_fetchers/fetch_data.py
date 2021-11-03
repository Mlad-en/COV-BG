from code_base.data_fetchers.data_fetchers import FetchEuroStatData


# TODO: Add handling if dynamic fetch fails
def fetch_data(data_type):
    data = FetchEuroStatData(data_type)
    return data.get_data()
