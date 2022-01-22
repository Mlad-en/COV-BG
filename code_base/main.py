from typing import Dict, Union, List

import pandas as pd

from code_base.data_calculations.calc_excess_mortality_pop import CalculateEurostatExcessMortalityToPopulation
from code_base.data_output.calc_bg_cov_info import CalcCovMortInfoBG
from code_base.data_output.calc_excess_mortality import CalcExcessMortalityPredicted, CalcEUCountryPop, CalcBGRegionPop
from code_base.data_savers.folder_structure import BaseFolderStructure
from code_base.data_savers.save_file import SaveFile, NameFile
from code_base.data_source.get_source_data import get_source_data
from code_base.data_bindings import data_types


def save_file(data: pd.DataFrame, file_type, file_subtype, year: Union[str, int], name_file: Dict):
    """

    :param data:
    :param file_type:
    :param file_subtype:
    :param year:
    :param name_file:
    :return:
    """
    name_file_helper = NameFile()
    name_file['age'] = name_file_helper.get_age_els(name_file['age'])
    file_name = name_file_helper.generate_name([val for val in name_file.values()])

    save_data = SaveFile()
    data_to_save = save_data.prep_multisheet_xlsx(data, 'Sex')

    file_location_helper = BaseFolderStructure()
    file_location = file_location_helper.get_output_folder_location(file_type, file_subtype, year)
    save_data.save_multisheet_xlsx(data_to_save, file_location, file_name)


def bg_generate_pred_exc_mort(years: List[int], age: List[List[str]], sex: List[str], start_week: int):
    mort_type = data_types.EurostatDataSets.MORTALITY_BY_SEX_AGE_REGION
    bg_mort_data = get_source_data(mort_type, analyze_years=years, region='BG')

    pop_type = data_types.InfostatDataSets.POP_BY_SEX_AGE_REG
    bg_pop_data = get_source_data(pop_type)

    for age_group in age:
        excess_mort = CalcExcessMortalityPredicted(data_type=mort_type, all_years=years)
        calc_mort = excess_mort.calculate(bg_mort_data, age_group, sex, start_week)

        eu_pop = CalcBGRegionPop(data_type=pop_type)
        calc_pop = eu_pop.calculate(bg_pop_data, age_group, sex)

        excess_mort_pop = CalculateEurostatExcessMortalityToPopulation()
        data = excess_mort_pop.calculate_excess_mortality(calc_mort, calc_pop, ['Location', 'Sex'])

        year = max(years)

        name_file = {
            'type': 'Predicted_Excess_Mortality_BG',
            'year': year,
            'sex': sex,
            'age': age_group,
        }

        save_file(data, 'ep', 'r', year, name_file)


def eu_generate_pred_exc_mort(years: List[int], age: List[List[str]], sex: List[str], start_week: int):
    mort_type = data_types.EurostatDataSets.MORTALITY_BY_SEX_AGE_COUNTRY
    eu_mort_data = get_source_data(mort_type, analyze_years=years)

    pop_type = data_types.EurostatDataSets.POP_BY_SEX_AGE_COUNTRY
    eu_pop_data = get_source_data(pop_type, analyze_years=years)

    for age_group in age:
        excess_mort = CalcExcessMortalityPredicted(data_type=mort_type, all_years=years)
        calc_mort = excess_mort.calculate(eu_mort_data, age_group, sex, start_week)
        eu_pop = CalcEUCountryPop(data_type=pop_type)
        calc_pop = eu_pop.calculate(eu_pop_data, age_group, sex)

        excess_mort_pop = CalculateEurostatExcessMortalityToPopulation()
        data = excess_mort_pop.calculate_excess_mortality(calc_mort, calc_pop, ['Location', 'Sex'])

        year = max(years)

        name_file = {
            'type': 'Predicted_Excess_Mortality_EU',
            'year': year,
            'sex': sex,
            'age': age_group,
        }

        save_file(data, 'ep', 'c', year, name_file)


def eu_generate_pred_perweek_exc_mort(years: List[int], start_week: int):
    age = ['Total']
    sex = ['Total']
    year = max(years)

    mort_type = data_types.EurostatDataSets.MORTALITY_BY_SEX_AGE_COUNTRY
    eu_mort_data = get_source_data(mort_type, analyze_years=years)
    excess_mort = CalcExcessMortalityPredicted(data_type=mort_type, all_years=years)
    calc_mort = excess_mort.calculate(eu_mort_data, age, sex, start_week, group_by='slw', predict_on='slw')
    calc_mort = calc_mort.loc[calc_mort['Location'] == 'Bulgaria']

    covid_mort = data_types.CoronaVirusBGDataSets.GENERAL
    covid_mort = get_source_data(covid_mort)
    calc_covd_mort = CalcCovMortInfoBG(data_types.CoronaVirusBGDataSets.GENERAL, year)
    covid_mort = calc_covd_mort.calculate(covid_mort)

    df = calc_mort.merge(covid_mort, on=['Week'])
    df.drop(['STANDARD_DEVIATION', 'Z-Score(95%)', 'Lower_bound_Mean/Expected_Mortality',
             'Upper_bound_Mean/Expected_Mortality', 'P_Score', 'P_Score_fluctuation', 'Mean/Expected_Mortality ±',
             'P_Score ±', 'Year', 'Cases_Last_24_Cases', 'Tests_Last_24_Done'], axis=1, inplace=True)

    name_file = {
        'type': 'Predicted_WEEKLY_Excess_Mortality_EU',
        'year': year,
        'sex': sex,
        'age': age,
    }

    save_file(df, 'ep', 'c', year, name_file)


def bg_generate_pred_perweek_exc_mort(years: List[int], start_week: int):
    age = ['Total']
    sex = ['Total']
    year = max(years)

    mort_type = data_types.EurostatDataSets.MORTALITY_BY_SEX_AGE_REGION
    bg_mort_data = get_source_data(mort_type, analyze_years=years, region='BG')
    excess_mort = CalcExcessMortalityPredicted(data_type=mort_type, all_years=years)
    calc_mort = excess_mort.calculate(bg_mort_data, age, sex, start_week, group_by='slw', predict_on='slw')


    covid_mort = data_types.CoronaVirusBGDataSets.GENERAL
    covid_mort = get_source_data(covid_mort)
    calc_covd_mort = CalcCovMortInfoBG(data_types.CoronaVirusBGDataSets.GENERAL, year)
    covid_mort = calc_covd_mort.calculate(covid_mort)

    df = calc_mort.merge(covid_mort, on=['Week'])

    name_file = {
        'type': 'Predicted_WEEKLY_Excess_Mortality_BG',
        'year': year,
        'sex': sex,
        'age': age,
    }

    save_file(df, 'ep', 'r', year, name_file)


if __name__ == '__main__':
    eu_generate_pred_exc_mort([2015, 2016, 2017, 2018, 2019, 2020], [['Total']], ['Female', 'Male', 'Total'], 10)
    bg_generate_pred_exc_mort([2015, 2016, 2017, 2018, 2019, 2020], [['Total']], ['Female', 'Male', 'Total'], 10)
