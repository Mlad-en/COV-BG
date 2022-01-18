from code_base.data_wrangling.wrangling_info.cvbg_wrangling_info import CVBGWranglingInfo


class CalcCovMortInfoBG:

    def __init__(self, data_type, year: int):
        self.wrangling_strategy = CVBGWranglingInfo(data_type).wrangling_strategy(year)

    def calculate(self, clean_data):
        clean_data = self.wrangling_strategy.filter_data(clean_data)
        clean_data = self.wrangling_strategy.group_data(clean_data)

        return clean_data

