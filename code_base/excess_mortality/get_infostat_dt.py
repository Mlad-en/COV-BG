import os
import time
from typing import List

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from webdriver_manager.chrome import ChromeDriverManager

from code_base.excess_mortality.folder_constants import *
from code_base.excess_mortality.url_constants import INFOSTAT_DATA


class DownloadInfostatDT:
    def __init__(self, data_type):
        if data_type not in INFOSTAT_DATA['pages']:
            raise ValueError(f'Incorrect data_type selected. Available data types are: {", ".join(INFOSTAT_DATA["pages"].key())}')

        # Set download locations
        self.raw_file_loc = source_infostat_raw
        self.clean_file_loc = source_infostat_cleaned

        self.preferences = {"download.default_directory": self.raw_file_loc,
                            "download.prompt_for_download": False,
                            "directory_upgrade": True,
                            "safebrowsing.enabled": True}

        # If additional Data types are added, update the exclude_params property's exc_vars mapper.
        self.data_type = data_type
        # Generate url
        self.url = INFOSTAT_DATA['main'] + INFOSTAT_DATA['pages'][self.data_type]

    @property
    def exclude_params(self):
        exc_vars = {
            'bg_pop_by_age_sex_reg': {
                'start_year': 2001,
                'end_year': 2020,
                'additional': ['Urban', 'Rural'],
            },
            'mortality_by_age_sex_mun': {
                'start_year': 2000,
                'end_year': 2015,
                'additional': []
            }
        }
        exclude_vars = [str(year) for year in range(exc_vars[self.data_type]['start_year'], exc_vars[self.data_type]['end_year'])]
        exclude_vars.extend(exc_vars[self.data_type]['additional'])

        return exclude_vars

    def get_all_dwnld_files(self):
        return os.listdir(self.raw_file_loc)

    def fetch_infostat_data(self) -> List:
        # Silence Webdriver Manager console logging.
        os.environ["WDM_LOG_LEVEL"] = '0'

        # Run Chrome browser in headless mode.
        options = Options()
        options.add_experimental_option("prefs", self.preferences)
        options.add_argument('--headless')
        browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        browser.get(self.url)
        browser.maximize_window()

        # Change webpage language to English from Bulgarian default.
        change_lang = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[text()="EN"]')))
        change_lang.click()

        time.sleep(5)

        # Search for and click the "Check All" checkboxes for all parameters.
        checkbox = browser.find_elements_by_xpath('//*/thead/tr/th[1]/div/div[2]/span')
        for el in checkbox:
            el.click()

        # Uncheck all Checkboxes that are NOT required
        for el in self.exclude_params:
            exclude_point = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, f'//span[text()="{el}"]/../../td[1]/div/div/span')))
            exclude_point.click()

        time.sleep(5)

        # Request Data
        browser.find_elements_by_xpath('//*[text()="Send"]')[1].click()
        # Wait for results page
        current_page = browser.current_url
        WebDriverWait(browser, 15).until(EC.url_changes(current_page))

        # List out files in directory before download
        initial_dwnld_files = self.get_all_dwnld_files()

        # Request data download in xlsx format
        request_data = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[text()="Download"]')))
        request_data.click()
        request_data = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[text()="XLSX"]')))
        request_data.click()

        # Hold browser open until download complete or 22 seconds elapse.
        time.sleep(2)
        counter = 0
        while [el for el in self.get_all_dwnld_files() if 'crdownload' in el] and counter < 20:
            counter += 1
            time.sleep(1)

        browser.quit()

        return [fl for fl in self.get_all_dwnld_files() if fl not in initial_dwnld_files]

    def rename_and_move_file(self, files: List, new_file_name: str) -> str:
        if files:
            raw_file = files[0]
            raw_file_path = os.path.join(self.raw_file_loc, raw_file)
            cleaned_file = os.path.join(self.clean_file_loc, new_file_name+'.xlsx')
            os.replace(raw_file_path, cleaned_file)
            return cleaned_file
        else:
            raise ValueError('Empty File List given as files argument.')


if __name__ == '__main__':
    c = DownloadInfostatDT('mortality_by_age_sex_mun')
    file = c.fetch_infostat_data()
    c.rename_and_move_file(file, 'infostat_mortality_by_age_sex_mun')

    c = DownloadInfostatDT('bg_pop_by_age_sex_reg')
    file = c.fetch_infostat_data()
    bg_population_raw = c.rename_and_move_file(file, 'infostat_bg_pop_by_age_sex_reg')