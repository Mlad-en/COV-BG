from code_base.official_bg_data.get_by_region_data import GetOfficialBGStats
from code_base.official_bg_data.folder_constants import source_official_bg_region_data

if __name__ == '__main__':
    c = GetOfficialBGStats(data_type='by_region')
    file = c.get_by_region_data()
    c.save_df(file,
              location=source_official_bg_region_data,
              file_name='By_region_case_cumulative',
              method='csv')