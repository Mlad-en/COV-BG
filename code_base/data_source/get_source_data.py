import pandas as pd

from code_base.data_bindings.data_types import CoronaVirusBGDataSets, InfostatDataSets, EurostatDataSets
from code_base.data_cleaners.clean_data import clean_data
from code_base.data_fetchers.fetch_data import fetch_data
from code_base.data_scrapers.scrape_data import scrape_data


def get_raw_source_data(data_type):
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

    return raw_data_getter(data_type)


def get_source_data(data_type, **additional_params):
    raw_data = get_raw_source_data(data_type)
    data = clean_data(data_type, raw_data, **additional_params)
    return data


if __name__ == '__main__':
    years = [2015, 2016, 2017, 2018, 2019, 2021]
    print(get_source_data(InfostatDataSets.MORTALITY_BY_SEX_AGE_MUN))

