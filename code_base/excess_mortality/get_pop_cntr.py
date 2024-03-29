import warnings
from typing import List, Optional
from os import path

import pandas as pd

from code_base.excess_mortality.decode_args import INFOSTAT_DECODE_AGE_GROUPS
from code_base.excess_mortality.scraping_constants import BG_MUNICIPALITIES, DECODE_REGION
from code_base.pyll.folder_constants import source_pop_data
from code_base.utils.common_query_params import ages_all


def get_bg_pop(file: str, sex: Optional[List] = None, age: Optional[List] = None, agg_agg: bool = True) -> pd.DataFrame:
    """
    :param file: Raw file that contains population data for Bulgaria.
    :param sex: Filters data by sex variables ['Female', 'Male']. If not given, default will be 'Total'
    :param age: Filters data by age variables (e.g. ['(30-34)', '(35-39)']. If not given, default will be 'Total'
    :param agg_agg:
    :return: Returns a dataframe that contains population data for Bulgaria, filtered for age and sex variables.
    """
    # Catch and suppress UserWarning from openpyxl about "Workbook contains no default style".
    warnings.simplefilter('ignore', category=UserWarning)

    df = pd.read_excel(file, sheet_name='Sheet0', engine='openpyxl', skiprows=3)

    # Remove Year column
    df.drop(df.columns[0], axis=1, inplace=True)
    # Remove bottom rows that contain a legend to the dataset
    df.dropna(how='any', inplace=True)
    # Normalize columns to be merged with other datasets more readily
    df.rename(columns={df.columns[0]: 'Location', df.columns[1]: 'Age'}, inplace=True)

    # Normalize Age to other data sets like the Eurostat ones.
    df['Age'] = df.apply(lambda x: INFOSTAT_DECODE_AGE_GROUPS.get(x['Age']), axis=1)
    df['Location'] = df.apply(lambda x: 'Sofia (stolitsa)' if x['Location'] == 'Sofia-grad' else x['Location'], axis=1)

    # Convert the Total, Male and Female columns to rows, and their values transposed to a new column: Population
    df = df.melt(id_vars=['Location', 'Age'], value_vars=['Total', 'Male', 'Female'], var_name='Sex',
                 value_name='Population')

    # Remove all rows where the population is less than 1 - expressed as "-" in the dataset.
    drop_indexes = df[df['Population'] == '-'].index
    df.drop(drop_indexes, inplace=True)

    # filter age and sex groups
    sex = sex if sex else ['Total']
    age = age if age else ['Total']

    df = df[(df['Age'].isin(age)) & (df['Sex'].isin(sex))]

    # Convert column to integer and sum values. Needed due to the age group mappings - current dataset has age groups like:
    # 90-94, 95-100, 100+. All of these are converted to 90+, hence they need to be summed.
    df['Population'] = df['Population'].map(int)

    if agg_agg:
        df.drop('Age', axis=1, inplace=True)
        df = df.groupby(['Location', 'Sex'], as_index=False).sum('Population')
    else:
        df = df.groupby(['Location', 'Age', 'Sex'], as_index=False).sum('Population')

    return df


def get_bg_mun_pop(file: str) -> pd.DataFrame:
    df = pd.read_excel(file, sheet_name='Sheet0', skiprows=4)

    # Removes Legend At the bottom
    df.dropna(how='any', inplace=True)

    # Rename columns. First column is unnamed, hence referenced as df.columns[0]
    df.rename(columns={df.columns[0]: 'Location',
                       'Общо': 'Total',
                       'Мъже': 'Male',
                       'Жени': 'Female'}, inplace=True)

    # Translate municipality names
    df['Location'] = df['Location'].apply(lambda x: BG_MUNICIPALITIES.get(x))

    # add Region information
    df['Region'] = df.apply(lambda x: DECODE_REGION.get(x['Location']), axis=1)
    # Method will not fill in Byala since there are two municipalities in Bulgaria with that name - one in Ruse, and one in Varna.
    # To account for this Region is copied from neighbouring row.
    df['Region'] = df['Region'].fillna(method='backfill')

    # Convert the Total, Male and Female columns to rows, and their values transposed to a new column: Population
    df = df.melt(id_vars=['Location', 'Region'], value_vars=['Total', 'Male', 'Female'], var_name='Sex', value_name='Population')

    df['Population'] = df['Population'].map(int)

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