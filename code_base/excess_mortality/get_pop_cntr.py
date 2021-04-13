from typing import List
from os import path

import pandas as pd
import re
import requests as r

from code_base.excess_mortality.decode_args import NSI_DECODE_AGE_GROUPS, INFOSTAT_DECODE_AGE_GROUPS
from code_base.excess_mortality.url_constants import NSI_DATA
from code_base.pyll.folder_constants import source_pop_data
from code_base.utils.common_query_params import ages_all


def get_bg_pop(file: str, sex: List = ['Total'], age: List = ['Total']) -> pd.DataFrame:
    df = pd.read_excel(file, sheet_name='Sheet0', engine='openpyxl', skiprows=3)

    # Remove Year column
    df.drop(df.columns[0], axis=1, inplace=True)
    # Remove bottom rows that contain a legend to the dataset
    df.dropna(how='any', inplace=True)
    # Normalize columns to be merged with other datasets more readily
    df.rename(columns={df.columns[0]: 'Location', df.columns[1]: 'Age'}, inplace=True)

    # Normalize Age to other data sets like the Eurostat ones.
    df['Age'] = df.apply(lambda x: INFOSTAT_DECODE_AGE_GROUPS.get(x['Age']), axis=1)

    # Convert the Total, Male and Female columns to rows, and their values transposed to a new column: Population
    df = df.melt(id_vars=['Location', 'Age'], value_vars=['Total', 'Male', 'Female'], var_name='Sex',
                 value_name='Population')

    # Remove all rows where the population is less than 1 - expressed as "-" in the dataset.
    drop_indexes = df[df['Population'] == '-'].index
    df.drop(drop_indexes, inplace=True)

    # Convert column to integer and sum values. Needed due to the age group mappings - current dataset has age groups like:
    # 90-94, 95-100, 100+. All of these are converted to 90+, hence they need to be summed.
    df['Population'] = df['Population'].map(int)
    df.groupby(['Location', 'Age', 'Sex'], as_index=False).sum('Population')

    # filter age and sex groups
    df = df[(df['Age'].isin(age)) & (df['Sex'].isin(sex))]

    return df


def get_itl_pop(age_range: List = ages_all, sex: List = ['Total']) -> pd.DataFrame:
    # Data obtained from http://demo.istat.it/popres/download.php?anno=2020&lingua=eng
    file = r'demo.istat - Resident population by age, sex and marital status on 1st January 2020.csv'
    location = source_pop_data
    file_path = path.join(location, file)
    df = pd.read_csv(file_path)

    # Remove all irrelevant columns - relevant columns "Age", "Total Men", "Total Women" and "Total Men and Women"
    cols = ['Eta', 'Totale Maschi', 'Totale Femmine', 'Totale Maschi e Femmine']
    df.drop([col for col in df.columns if col not in cols], axis=1, inplace=True)

    # Total values are not needed, only actual ages, e.g. 1, 2, 3, etc.
    df.drop(df[df['Eta'] == 'Totale'].index, axis=0, inplace=True)

    columns = {'Eta': 'Age',
               'Totale Maschi': 'Male',
               'Totale Femmine': 'Female',
               'Totale Maschi e Femmine': 'Total'}
    df.rename(columns=columns, inplace=True)

    df['Age'] = df['Age'].map(int)

    # Aggregate data in increments of 5, with the uppermost group from 90 to an impossible age value to encapsulate
    # all ages above 90 in this group.
    bins = [0, 4, 9, 14, 19, 24, 29, 34, 39, 44, 49, 54, 59, 64, 69, 74, 79, 84, 89, 150]
    labels = ['(0-4)', '(5-9)', '(10-14)', '(15-19)', '(20-24)', '(25-29)',
              '(30-34)', '(35-39)', '(40-44)', '(45-49)', '(50-54)', '(55-59)',
              '(60-64)', '(65-69)', '(70-74)', '(75-79)', '(80-84)', '(85-89)', '(90+)']
    bins = pd.cut(df['Age'], bins=bins, include_lowest=True, labels=labels)
    df = df.groupby([bins]).agg({'Male': 'sum', 'Female': 'sum', 'Total': 'sum'})
    df.reset_index(inplace=True)

    # Convert the Total, Male and Female columns to rows, and their values transposed to a new column: Population
    df = df.melt(id_vars=['Age'], value_vars=['Male', 'Female', 'Total'], var_name='Sex', value_name='Population')

    # Add Location column to facilitate combining with other dataframes.
    df['Location'] = 'Italy'

    # filter age and sex groups
    df = df[(df['Age'].isin(age_range)) & df['Sex'].isin(sex)]

    return df


# Function no longer valid since NSI has implemented anti-scraping technology on their site - CloudFlare.
# def get_bg_pop_deprecated(sex: List = ['Total'], age: List = ['Total']):
#     url = NSI_DATA['main'] + NSI_DATA['pages']['bg_pop_by_age_sex_reg']
#     req = r.get(url)
#     df = pd.read_html(req.content)[0]
#     df.columns = [x[1] for x in df.columns]
#     df.rename(columns={'DistrictsMunicipalities': 'Location'}, inplace=True)
#     df = df.iloc[:, 0:4]
#
#     df['Location'] = ''
#     pattern = re.compile(r'\d')
#     for i in range(0, len(df)):
#         df.loc[i, 'Location'] = df.loc[i, 'DistrictsAge (years)'] if not re.findall(pattern, df.loc[
#             i, 'DistrictsAge (years)']) else df.loc[i - 1, 'Location']
#
#     df['DistrictsAge (years)'] = df.apply(lambda x:
#                                           'Total' if x['DistrictsAge (years)'] == x['Location']
#                                           else x['DistrictsAge (years)'],
#                                           axis=1)
#     df.rename(columns={'DistrictsAge (years)': 'Age'}, inplace=True)
#
#     df['Age'] = df.apply(lambda x: NSI_DECODE_AGE_GROUPS.get(x['Age']), axis=1)
#
#     df = df.melt(id_vars=['Location', 'Age'], value_vars=['Total', 'Male', 'Female'], var_name='Sex',
#                  value_name='Population')
#
#     df['Population'] = df['Population'].str.replace(r'\D+', '', regex=True)
#     drop_indexes = df[df['Population'] == ''].index
#     df.drop(drop_indexes, inplace=True)
#     df['Population'] = df['Population'].map(int)
#     df = df.groupby(['Location', 'Age', 'Sex'], as_index=False).sum('Population')
#     df = df[(df['Age'].isin(age)) & (df['Sex'].isin(sex))]
#     return df