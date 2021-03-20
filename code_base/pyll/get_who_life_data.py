import pandas as pd
import numpy as np

from code_base.utils.save_file_utils import SaveFile
from code_base.pyll.decode_loc_vars import EU_COUNTRIES_ISO_3_DECODES
from code_base.pyll.decode_vars import *
from code_base.pyll.url_constants import WHO_DATA


class GetWHOLifeData(SaveFile):
    def __init__(self):
        pass

    @staticmethod
    def get_life_tables_eu(location: str = 'EUR', year: str = '2019'):

        life_tables = WHO_DATA['api']['life_tables_europe']
        life_tables = life_tables.replace('###REGION###', location).replace('###YEAR###', year)
        url = WHO_DATA['main'] + life_tables

        df = pd.read_csv(url)

        drop_columns = ['GHO', 'PUBLISHSTATE', 'REGION',
                        'WORLDBANKINCOMEGROUP', 'Display Value',
                        'Low', 'High', 'Comments']
        df.drop(drop_columns, axis=1, inplace=True)

        df['AGEGROUP'] = df.apply(lambda x: DECODE_WHO_AGE_RANGES.get(x['AGEGROUP'], np.nan), axis=1)
        df['SEX'] = df.apply(lambda x: DECODE_WHO_GENDER_VARS.get(x['SEX'], np.nan), axis=1)
        df['COUNTRY'] = df.apply(lambda x: EU_COUNTRIES_ISO_3_DECODES.get(x['COUNTRY'], np.nan), axis=1)
        df.dropna(how='any', axis=0, inplace=True)

        return df.round(1)