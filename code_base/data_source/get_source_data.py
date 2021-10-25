import pandas as pd

from code_base.data_cleaners.cleaning_info.eurostat_cleaning_info import EurostatCleaningInfo
from code_base.data_cleaners.cleaning_info.infostat_cleaning_info import InfostatCleaningInfo
from code_base.data_fetchers.data_fetchers import FetchEuroStatData
from code_base.data_scrapers.scrape_infostat.scrape_infostat import ScrapeRawInfostatData


def get_eurostat_data(data_type: str, **additional_params) -> pd.DataFrame:
    """

    :param data_type:
    :param additional_params:
    :return:
    """
    data_type = data_type

    get_data = FetchEuroStatData(data_type)
    data = get_data.get_data()

    data_cleaning_info = EurostatCleaningInfo(data_type)
    cleaning_params = data_cleaning_info.cleaning_params(**additional_params)
    cleaning_strategy = data_cleaning_info.cleaning_strategy(data, **cleaning_params)
    clean_data = cleaning_strategy.clean_data()

    return clean_data


def get_infostat_data(data_type: str) -> pd.DataFrame:
    """

    :param data_type:
    :return:
    """
    data_type = data_type

    scrape_data = ScrapeRawInfostatData(data_type)
    data = scrape_data.get_data()

    data_cleaning_info = InfostatCleaningInfo(data_type)
    filter_by = data_cleaning_info.filter_df_by
    col_headers = data_cleaning_info.rename_headers
    melt_by = data_cleaning_info.melt_cols
    cleaning_strategy = data_cleaning_info.cleaning_strategy(data, filter_by, col_headers, melt_by)
    clean_data = cleaning_strategy.clean_data()

    return clean_data


if __name__ == '__main__':
    print(get_eurostat_data('excess_mortality_by_sex_age_country', analyze_years=[2015, 2016, 2017, 2018, 2019, 2020]))