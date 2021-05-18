from code_base.official_bg_data.get_bg_cov_mort import GetBGMort
from code_base.official_bg_data.get_official_bg_data import GetOfficialBGStats
from code_base.official_bg_data.folder_constants import *

if __name__ == '__main__':
    c = GetOfficialBGStats()
    file = c.get_by_region_data()
    c.save_df_to_file(file,
                      location=source_official_bg_region_data,
                      file_name='By_region_case_cumulative',
                      method='csv')
    file = c.get_tests_to_cases_by_week()
    c.save_df_to_file(file,
                      location=source_official_general_data,
                      file_name='Test_to_cases_by_week',
                      method='csv')

    dct = {'start_date': (2020, 7, 1),
           'end_date': (2021, 1, 1)}
    bg_mort = GetBGMort()
    bg_mort_raw_file = bg_mort.save_raw_mh_articles(dct)
    bg_mort.generate_per_person_mort_dt(bg_mort_raw_file, dct)

    dct = {'start_date': (2021, 1, 1),
           'end_date': (2021, 5, 18)}
    bg_mort = GetBGMort()
    bg_mort_raw_file = bg_mort.save_raw_mh_articles(dct)
    bg_mort.generate_per_person_mort_dt(bg_mort_raw_file, dct)