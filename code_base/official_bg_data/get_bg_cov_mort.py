from datetime import date, timedelta
from typing import Dict, Tuple, Generator, Union
import re

from bs4 import BeautifulSoup
import pandas as pd
import requests

from code_base.excess_mortality.folder_constants import source_cov_bg_auto
from code_base.official_bg_data.scraping_constants import *
from code_base.official_bg_data.url_constants import BG_MH_URL
from code_base.utils.save_file_utils import SaveFile


class GetBGMort(SaveFile):
    def __init__(self):
        self.source_loc = source_cov_bg_auto
        super().__init__()

    @staticmethod
    def generate_dates_between_periods(dates: Dict[str, Tuple[int, int, int]]) -> Generator[Tuple[str, str], None, None]:
        """
        :param dates: Periods should be provided in a Dictionary format as follows:
        {'start_date':(YEAR:int, MM:int, DD:int),
        'end_date': (YEAR:int, MM:int, DD:int)}
        E.g. start date: (2020,4,21) || end date: (2020,4,25)
        :return: Returns a generator of string start and end dates between given periods, incrementing by 1.
        End Date is excluded from the return generator.
        """

        start_date = date(*dates['start_date'])
        end_date = date(*dates['end_date'])
        delta = end_date - start_date
        for i in range(delta.days):
            start_range = start_date + timedelta(days=i)
            end_range = start_date + timedelta(days=i + 1)
            yield start_range.strftime('%d.%m.%Y'), end_range.strftime('%d.%m.%Y')

    @staticmethod
    def get_mh_articles(s_range: str, e_range: str) -> requests.models.Response:
        """
        :param s_range: Start range of the
        :param e_range:
        :return: Returns request response object of the Ministry of Health of Bulgaria website with Covid-19-related
        articles posted between a given date period.
        """
        URL = BG_MH_URL['main'] + BG_MH_URL['pages']['news']['landing_page']
        params = {
            BG_MH_URL['pages']['news']['page_params']['start_date']: s_range,
            BG_MH_URL['pages']['news']['page_params']['end_date']: e_range,
        }
        req = requests.get(URL, params=params)
        return req

    @staticmethod
    def parse_stats_article_links(req: requests.models.Response.content) -> Union[Tuple[str, str], Tuple[None, None]]:
        """
        :param req: Receives a
        :return: Returns a tuple of strings containing the title and link to articles containing Covid-19 statistics.
        If an article is found on the topic (Covid-19) but it's not about Covid-19 mortality then None tuple is returned.
        """
        soup = BeautifulSoup(req, 'lxml')
        stats_article = soup.find_all('a', text=re.compile(MH_TITLE_ARTICLE_PATTERN))
        if stats_article:
            article_link = BG_MH_URL['main'] + stats_article[0]['href']  # strips leading slash "/"
            title = stats_article[0].text
            return article_link, title
        else:
            return None, None

    @staticmethod
    def parse_article_text_and_date(article_link: str) -> Tuple[str, str]:
        """
        :param article_link: URL location to particular COVID-19  update from the Ministry of Health.
        :return: Returns a tuple containing the art_date and article text from a given article link.
        """
        req = requests.get(article_link)
        soup = BeautifulSoup(req.content, 'lxml')
        art_date = soup.find('time').text
        article_text = soup.find('div', class_='single_news').text

        return art_date, article_text

    def save_raw_mh_articles(self, period_dict: Dict[str, Tuple[int, int, int]]) -> str:
        """
        Function saves a csv file with all articles related to COVID between the provided period of the function input.
        The function will return the file path of the generated file.
        :param period_dict: Periods should be provided in a Dictionary format as follows:
        {'start_date':(YEAR, MM, DD),
        'end_date': (YEAR, MM, DD)}
        E.g. start date: (2020.04.20) || end date: (2020.04.25)
        :return: Returns the file name of the generated file, in the following format:
        MH_raw_article_text_from_{START_DATE}_to_{END_DATE}.csv
        """

        df = pd.DataFrame(columns=MH_RAW_ARTICLE_TEXT_COLUMNS)

        for start_range, end_range in self.generate_dates_between_periods(period_dict):
            page = self.get_mh_articles(start_range, end_range)
            page_content = self.parse_stats_article_links(page.content)
            link, title = page_content

            if link:
                dt, article_text = self.parse_article_text_and_date(link)
            else:
                dt, article_text = None, None

            data = {
                'date': start_range,
                'title': title,
                'link': link,
                'dt_str': dt,
                'article_text': article_text
            }
            df = df.append(data, ignore_index=True)

        file_name = f'bg_mh_raw_article_text_from_{period_dict["start_date"]}_to_{period_dict["end_date"]}'
        file_location = self.save_df_to_file(df=df, location=self.source_loc,file_name=file_name, method='csv')

        return file_location

    @staticmethod
    def generate_raw_mortality_per_person(original_file: str) -> pd.DataFrame:
        '''
        Function parses articles from a provided csv file and generates a dataframe with raw person information about
        persons that have passed from COVID-19.
        :param original_file: Receives a file path to csv file with articles about COVID from the Bulgarian Ministry of Health.
        :return: Returns a Data frame with person records about persons that have passed from COVID-19.
        '''

        raw_per_person_df = pd.DataFrame(columns=MH_PER_PERSON_COLUMNS)
        raw_article_text_df = pd.read_csv(original_file)
        raw_article_text_df.dropna(axis=0, how='any', inplace=True)

        for index in raw_article_text_df.index:
            article_text = raw_article_text_df.at[index, 'article_text']
            date = raw_article_text_df.at[index, 'date']
            # Creates an iterable looking for fatalities based on mention of gender, which is a convention used in the articles.
            mortality_groups_extract = re.finditer(MH_SPIT_BY_GENDER_ARTICLE_PATTERN, article_text)
            start_ranges = [mortality_group.start() for mortality_group in mortality_groups_extract]

            if start_ranges:
                mortality_snippet = []

                if len(start_ranges) > 1:
                    for index in range(0, len(start_ranges) - 1):
                        article_start_index = start_ranges[index]
                        article_end_index = start_ranges[index + 1]
                        mortality_line = article_text[article_start_index:article_end_index]
                        mortality_snippet.append(mortality_line)

                final_line_start = start_ranges[-1]
                final_line_end = article_text.find('\n', final_line_start)
                mortality_line = article_text[final_line_start:final_line_end]
                mortality_snippet.append(mortality_line)

                for person_mortality in mortality_snippet:
                    data = {
                        'date': date,
                        'person_data_raw': person_mortality.strip()
                    }
                    raw_per_person_df = raw_per_person_df.append(data, ignore_index=True)

        return raw_per_person_df

    def generate_per_person_mort_dt(self, file_loc: str, dates: Dict) -> str:
        """
        Function receives a file location with raw article data and parses it for comorbities, age and sex of the person.
        The function saves a csv file of the generated dataframe and returns the file path to the file.
        :param dates: Periods should be provided in a Dictionary format as follows:
        {'start_date':(YEAR:int, MM:int, DD:int),
        'end_date': (YEAR:int, MM:int, DD:int)}
        E.g. start date: (2020,4,21) || end date: (2020,4,25)
        :param file_loc: Receives a file location with raw per person data scraped from the Bulgarian Ministry of Health.
        :return: Returns the file path of the created csv file.
        """

        df = self.generate_raw_mortality_per_person(file_loc)

        for index in df.index:
            person_data = df.at[index, 'person_data_raw'].lower()

            for attr_name, attr_values in MH_PER_PERSON_COMORBIDITY.items():
                for attr in attr_values:
                    if attr in person_data:
                        df.at[index, attr_name] = 'Y'
                        break
                else:
                    df.at[index, attr_name] = 'N'

            no_comorbidity = 'Y' if 'придружаващи' in person_data \
                                    and ('без' in person_data or 'няма' in person_data
                                         or 'не са въведени' in person_data
                                         or 'липсва информация' in person_data) \
                else ''
            df.at[index, 'no_comorbidity'] = no_comorbidity

            unknown = 'UNK'
            gender = 'Male' if 'мъж' in person_data else 'Female' if 'жена' in person_data else unknown
            df.at[index, 'gender'] = gender

            try:
                age = re.findall(MH_PER_PERSON_AGE_PATTERN, person_data)[0]
                df.at[index, 'age'] = age
            except (TypeError, IndexError):
                continue

        file_name = f'bg_mh_per_person_mortality_{dates["start_date"]}_{dates["end_date"]}'
        file_location = self.save_df_to_file(df=df, location=self.source_loc, file_name=file_name, method='csv')

        return file_location