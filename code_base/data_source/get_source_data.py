from code_base.data_bindings import data_types
from code_base.data_cleaners.clean_data import clean_data
from code_base.data_fetchers.fetch_data import fetch_data
from code_base.data_scrapers.scrape_data import scrape_data


def get_raw_source_data(data_type, **additional_params):
    mapping = {
        data_types.CoronaVirusBGDataSets: scrape_data,
        data_types.InfostatDataSets: scrape_data,
        data_types.EurostatDataSets: fetch_data,
        data_types.WHODataSets: fetch_data,
        data_types.LocalDataSets: fetch_data,
    }
    data_type = data_type
    data_type_class = data_type.__class__
    raw_data_getter = mapping.get(data_type_class)

    if not raw_data_getter:
        raise ValueError(f'Could not find data scraper with parameter: {str(data_type)}')

    return raw_data_getter(data_type, data_type_class=data_type_class, **additional_params)


def get_source_data(data_type, **additional_params):
    raw_data = get_raw_source_data(data_type, **additional_params)
    data = clean_data(data_type, raw_data, **additional_params)
    return data


if __name__ == '__main__':
    data = get_source_data(data_types.LocalDataSets.CVD_Europe)
    print(data)