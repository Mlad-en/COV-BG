from typing import List

import pandas as pd
import re
import requests as r

from code_base.excess_mortality.decode_args import NSI_DECODE_AGE_GROUPS
from code_base.excess_mortality.url_constants import NSI_DATA


def get_bg_pop(sex: List = ['Total'], age: List = ['Total']):
    url = NSI_DATA['main'] + NSI_DATA['pages']['bg_pop_by_age_sex_reg']
    req = r.get(url)
    df = pd.read_html(req.content)[0]
    df.columns = [x[1] for x in df.columns]
    df.rename(columns={'DistrictsMunicipalities': 'Location'}, inplace=True)
    df = df.iloc[:, 0:4]

    df['Location'] = ''
    pattern = re.compile('\d')
    for i in range(0, len(df)):
        df.loc[i, 'Location'] = df.loc[i, 'DistrictsAge (years)'] if not re.findall(pattern, df.loc[
            i, 'DistrictsAge (years)']) else df.loc[i - 1, 'Location']

    df['DistrictsAge (years)'] = df.apply(lambda x:
                                          'Total' if x['DistrictsAge (years)'] == x['Location']
                                          else x['DistrictsAge (years)'],
                                          axis=1)
    df.rename(columns={'DistrictsAge (years)': 'Age'}, inplace=True)

    df['Age'] = df.apply(lambda x: NSI_DECODE_AGE_GROUPS.get(x['Age']), axis=1)

    df = df.melt(id_vars=['Location', 'Age'], value_vars=['Total', 'Male', 'Female'], var_name='Sex',
                 value_name='Population')

    df['Population'] = df['Population'].str.replace(r'\D+', '', regex=True)
    drop_indexes = df[df['Population'] == ''].index
    df.drop(drop_indexes, inplace=True)
    df['Population'] = df['Population'].map(int)
    df = df.groupby(['Location', 'Age', 'Sex'], as_index=False).sum('Population')
    df = df[(df['Age'].isin(age)) & (df['Sex'].isin(sex))]
    return df