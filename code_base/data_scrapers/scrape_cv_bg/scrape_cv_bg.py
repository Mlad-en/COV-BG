import pandas as pd

from code_base.data_scrapers.scrape_cv_bg.scrape_cv_bg_info import CoronaVirusBGFileInfo


class GetOfficialBGStats:

    def __init__(self, data_type):
        self.data_type = data_type

    def get_data(self) -> pd.DataFrame:
        data_info = CoronaVirusBGFileInfo(self.data_type)
        df = pd.read_csv(data_info.file_url)
        df.rename(columns=data_info.data_headers, inplace=True)
        df['Date'] = pd.to_datetime(df['Date'], format='%Y/%m/%d')

        return df