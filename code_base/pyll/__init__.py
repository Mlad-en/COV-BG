from code_base.pyll.folder_constants import source_WHO_life_data
from code_base.pyll.get_who_life_data import GetWHOLifeData

if __name__ == '__main__':
    c = GetWHOLifeData()
    file = c.get_life_tables_eu()
    c.save_df_to_file(df=file, location=source_WHO_life_data, file_name='WHO_Life_tables_Europe')