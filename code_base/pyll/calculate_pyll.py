import pandas as pd

from code_base.excess_mortality.calc_excess_mortality import CalcExcessMortality
from code_base.excess_mortality.common_query_params import exclude_cntrs
from code_base.pyll import GetWHOLifeData
from code_base.utils.save_file_utils import SaveFile


class CalcExcessMortPyll(SaveFile):
    def __init__(self):
        pass

    @property
    def get_excess_mortality(self) -> pd.DataFrame:
        eu_mortality = CalcExcessMortality()
        mortality = eu_mortality.get_mortality_df
        exc_mort = eu_mortality.calc_excess_mortality(eu_mortality.clean_eu_data(mortality, exclude_cntrs), add_age=True)

        relevant_cols = ['Age', 'Sex', 'Location', 'Excess_mortality_Mean', 'Excess_mortality_fluc']
        exc_mort.drop(columns=[col for col in exc_mort if col not in relevant_cols], inplace=True)

        return exc_mort

    @property
    def get_life_exp_eu(self):
        eu_lf = GetWHOLifeData()
        return eu_lf.get_life_tables_eu()

    def calculate_pyll_all_ages(self):
        merge_on = ['Age', 'Sex', 'Location']
        pyll_dt = self.get_life_exp_eu.merge(self.get_excess_mortality, on=merge_on)
        pyll_dt['PYLL'] = pyll_dt.apply(
            lambda x: x['Life_Expectancy'] * x['Excess_mortality_Mean'] if x['Excess_mortality_Mean'] > 0 else 0,
            axis=1).round(1)

        return pyll_dt

