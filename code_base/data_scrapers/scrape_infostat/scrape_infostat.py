import pandas as pd

from code_base.data_scrapers.scrape_infostat.scrape_infostat_file_info import InfostatFileInfo
from code_base.data_scrapers.utils import *


class ScrapeRawInfostatData:
    """
    Class provides a method to scrape data from Infostat (Bulgaria's National Statistical Institute open-data portal)
    based on the file type that is required.
    """
    def __init__(self, file_type):
        self.file_info = InfostatFileInfo(file_type)

    def get_data(self, headless_browser: bool = True) -> List:
        """
        Function used to scrape data from Infostat. The function scrapes all tables on the results page of Infostat,
        hence results from this scraping require further processing/ filtering.
        :param headless_browser: Bool value, default is true. If set to false, web scraping is visible.
        :return: Function returns a list of Dataframes.
        """

        url = self.file_info.file_url
        file_language = self.file_info.file_language
        file_filters = self.file_info.file_filters

        with launch_browser(url, headless=headless_browser) as browser:
            page_actions = PageObjectActions(browser)

            request_strategy = self.file_info.request_strategy(page_actions, file_language, file_filters, url)
            request_strategy.request_data()

            dfs = pd.read_html(browser.page_source)

        return dfs
