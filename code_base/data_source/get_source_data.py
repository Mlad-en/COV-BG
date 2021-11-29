import pandas as pd

from code_base.data_bindings.data_types import CoronaVirusBGDataSets, InfostatDataSets, EurostatDataSets
from code_base.data_cleaners.clean_data import clean_data
from code_base.data_fetchers.fetch_data import fetch_data
from code_base.data_scrapers.scrape_data import scrape_data


def get_raw_source_data(data_type, **additional_params):
    mapping = {
        CoronaVirusBGDataSets: scrape_data,
        InfostatDataSets: scrape_data,
        EurostatDataSets: fetch_data
    }
    data_type = data_type
    data_type_class = data_type.__class__
    raw_data_getter = mapping.get(data_type_class)

    if not raw_data_getter:
        raise ValueError(f'Could not find data scraper with parameter: {str(data_type)}')

    if not data_type_class == EurostatDataSets:
        return raw_data_getter(data_type, data_type_class=data_type_class, **additional_params)

    return raw_data_getter(data_type)


def get_source_data(data_type, **additional_params):
    raw_data = get_raw_source_data(data_type, **additional_params)
    data = clean_data(data_type, raw_data)
    return data


