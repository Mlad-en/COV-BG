from code_base.data_bindings.data_types import CoronaVirusBGDataSets, InfostatDataSets
from code_base.data_scrapers.scrape_cv_bg.scrape_cv_bg import GetOfficialBGStats
from code_base.data_scrapers.scrape_infostat.scrape_infostat import ScrapeRawInfostatData


def scrape_data(data_type, data_type_class, **additional_params):
    mapping = {
        CoronaVirusBGDataSets: GetOfficialBGStats,
        InfostatDataSets: ScrapeRawInfostatData,
    }
    scraper = mapping[data_type_class](data_type)
    data = scraper.get_data(**additional_params)
    return data
