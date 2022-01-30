import pytest

from code_base.data_bindings.data_types import InfostatDataSets
from code_base.data_scrapers.scrape_infostat.scrape_infostat import ScrapeRawInfostatData


@pytest.mark.parametrize('data_type',
                         [InfostatDataSets.POP_BY_SEX_AGE_REG,
                          InfostatDataSets.AVG_LIFE_EXPECTANCY_BY_SEX,
                          InfostatDataSets.LIFE_EXPECTANCY_BY_SEX,
                          InfostatDataSets.MORTALITY_BY_SEX_AGE_MUN,
                          InfostatDataSets.POP_BY_MUNICIPALITY])
def test_url_response(data_type):
    scrape_data = ScrapeRawInfostatData(data_type)
    data = scrape_data.get_data()
    assert data
