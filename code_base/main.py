import os
from typing import Dict, Union, List

import pandas as pd

from code_base.data_calculations.calc_asyr import CalcASYR
from code_base.data_calculations.calc_excess_mortality_pop import CalculateEurostatExcessMortalityToPopulation
from code_base.data_calculations.calc_pyll import CalcPYLL
from code_base.data_calculations.calc_wyll import CalcWYLL
from code_base.data_output.calc_bg_cov_info import CalcCovMortInfoBG
from code_base.data_output.calc_excess_mortality import CalcExcessMortalityPredicted, CalcEUCountryPop, CalcBGRegionPop
from code_base.data_savers.folder_structure import BaseFolderStructure
from code_base.data_savers.save_file import SaveFile, NameFile
from code_base.data_source.get_source_data import get_source_data
from code_base.data_bindings import data_types


def save_file(data: pd.DataFrame, file_dir, name_file: Dict):
    """

    :param data:
    :param file_dir:
    :param year:
    :param name_file:
    :return:
    """

    name_file_helper = NameFile()
    if 'age' in name_file.keys():
        name_file['age'] = name_file_helper.get_age_els(name_file['age'])
    file_name = name_file_helper.generate_name([val for val in name_file.values()])

    save_data = SaveFile()
    data_to_save = save_data.prep_multisheet_xlsx(data, 'Sex')

    save_data.save_multisheet_xlsx(data_to_save, file_dir, file_name)


def bg_generate_pred_exc_mort(years: List[int], age: List[List[str]], sex: List[str], start_week: int):
    """

    :param years:
    :param age:
    :param sex:
    :param start_week:
    :return:
    """

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

        file_loc = os.path.join(BaseFolderStructure.REGIONS_EM, str(year))
        save_file(data, file_loc, name_file)


def eu_generate_pred_exc_mort(years: List[int], age: List[List[str]], sex: List[str], start_week: int):
    """

    :param years:
    :param age:
    :param sex:
    :param start_week:
    :return:
    """

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

        file_loc = os.path.join(BaseFolderStructure.COUNTRIES_EM, str(year))
        save_file(data, file_loc, name_file)


def eu_generate_pred_perweek_exc_mort(years: List[int], start_week: int):
    """

    :param years:
    :param start_week:
    :return:
    """

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

    file_loc = os.path.join(BaseFolderStructure.COUNTRIES_EM, str(year))
    save_file(df, file_loc, name_file)


def bg_generate_pred_perweek_exc_mort(years: List[int], start_week: int):
    """

    :param years:
    :param start_week:
    :return:
    """

    age = ['Total']
    sex = ['Total']
    year = max(years)

    mort_type = data_types.EurostatDataSets.MORTALITY_BY_SEX_AGE_REGION
    bg_mort_data = get_source_data(mort_type, analyze_years=years, region='BG')
    excess_mort = CalcExcessMortalityPredicted(data_type=mort_type, all_years=years)
    calc_mort = excess_mort.calculate(bg_mort_data, age, sex, start_week, group_by='slw', predict_on='slw')

    covid_mort = data_types.CoronaVirusBGDataSets.GENERAL
    covid_mort = get_source_data(covid_mort)
    calc_covid_mort = CalcCovMortInfoBG(data_types.CoronaVirusBGDataSets.GENERAL, year)
    covid_mort = calc_covid_mort.calculate(covid_mort)

    df = calc_mort.merge(covid_mort, on=['Week'])

    name_file = {
        'type': 'Predicted_WEEKLY_Excess_Mortality_BG',
        'year': year,
        'sex': sex,
        'age': age,
    }

    file_loc = os.path.join(BaseFolderStructure.REGIONS_EM, str(year))
    save_file(df, file_loc, name_file)


def generate_eu_pyll(years: List[int], ages: List[int], sexes: List[str], from_week: int, static_over_90: bool):
    pyll = CalcPYLL(years, ages, sexes, from_week, static_over_90).calculate()

    year = max(years)
    name_file = {
        'type': 'EU_PYLL',
        'year': year,
        'sex': sexes,
        'age': ages,
        'static_over_90': f'static_over_90: {static_over_90}'
    }

    file_loc = BaseFolderStructure.PYLL_EU
    save_file(pyll, file_loc, name_file)


def generate_eu_wyll(years, sexes, from_week):
    wyll = CalcWYLL(years, sexes, from_week).calculate()

    year = max(years)
    name_file = {
        'type': 'EU_WYLL',
        'year': year,
        'sex': sexes,
    }

    file_loc = BaseFolderStructure.PYLL_EU
    save_file(wyll, file_loc, name_file)


def generate_eu_asyr(years: List[int], ages: List[int], sexes: List[str], from_week: int, static_over_90: bool):
    """

    :param years:
    :param ages:
    :param sexes:
    :param from_week:
    :param static_over_90:
    :return:
    """

    asyr = CalcASYR(years, ages, sexes, from_week, static_over_90).calculate()

    year = max(years)
    name_file = {
        'type': 'EU_ASYR',
        'year': year,
        'sex': sexes,
        'age': ages,
        'static_over_90': f'static_over_90: {static_over_90}'
    }

    file_loc = BaseFolderStructure.PYLL_EU
    save_file(asyr, file_loc, name_file)


if __name__ == '__main__':
    from code_base.data_bindings.age_group_translations import AGE_BINDINGS

    # eu_generate_pred_exc_mort([2015, 2016, 2017, 2018, 2019, 2020], [['Total']], ['Female', 'Male', 'Total'], 10)
    # bg_generate_pred_exc_mort([2015, 2016, 2017, 2018, 2019, 2020], [['Total']], ['Female', 'Male', 'Total'], 10)
    sex = ['Female', 'Male', 'Total']
    years = [2015, 2016, 2017, 2018, 2019, 2020]
    start_week = 10
    static_over_90 = True

    ages_0_89 = [AGE_BINDINGS.AGE_00_04, AGE_BINDINGS.AGE_05_09, AGE_BINDINGS.AGE_10_14,
                 AGE_BINDINGS.AGE_15_19, AGE_BINDINGS.AGE_20_24, AGE_BINDINGS.AGE_25_29,
                 AGE_BINDINGS.AGE_30_34, AGE_BINDINGS.AGE_35_39, AGE_BINDINGS.AGE_40_44,
                 AGE_BINDINGS.AGE_45_49, AGE_BINDINGS.AGE_50_54, AGE_BINDINGS.AGE_55_59,
                 AGE_BINDINGS.AGE_60_64, AGE_BINDINGS.AGE_65_69, AGE_BINDINGS.AGE_70_74,
                 AGE_BINDINGS.AGE_75_79, AGE_BINDINGS.AGE_80_84, AGE_BINDINGS.AGE_85_89]

    all_ages = [AGE_BINDINGS.AGE_00_04, AGE_BINDINGS.AGE_05_09, AGE_BINDINGS.AGE_10_14,
                AGE_BINDINGS.AGE_15_19, AGE_BINDINGS.AGE_20_24, AGE_BINDINGS.AGE_25_29,
                AGE_BINDINGS.AGE_30_34, AGE_BINDINGS.AGE_35_39, AGE_BINDINGS.AGE_40_44,
                AGE_BINDINGS.AGE_45_49, AGE_BINDINGS.AGE_50_54, AGE_BINDINGS.AGE_55_59,
                AGE_BINDINGS.AGE_60_64, AGE_BINDINGS.AGE_65_69, AGE_BINDINGS.AGE_70_74,
                AGE_BINDINGS.AGE_75_79, AGE_BINDINGS.AGE_80_84, AGE_BINDINGS.AGE_85_89,
                AGE_BINDINGS.AGE_GE90]

    print("Starting Eu WYLL")
    generate_eu_wyll(years, sex, start_week)
    print("Finished Eu WYLL")

    print("Starting Eu ASYR")
    generate_eu_asyr(years, ages_0_89, sex, start_week, static_over_90)
    print("Finished Eu ASYR")

    print("Starting Eu PYLL")
    generate_eu_pyll(years, ages_0_89, sex, start_week, static_over_90)
    print("Finished Eu PYLL")

    print("Starting Eu ASYR")
    generate_eu_asyr(years, all_ages, sex, start_week, static_over_90)
    print("Finished Eu ASYR")

    print("Starting Eu PYLL")
    generate_eu_pyll(years, all_ages, sex, start_week, static_over_90)
    print("Finished Eu PYLL")
