from code_base.official_bg_data.get_official_bg_data import GetOfficialBGStats
from code_base.official_bg_data.folder_constants import *

if __name__ == '__main__':
    c = GetOfficialBGStats()
    # file = c.get_data()
    # print(file)
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