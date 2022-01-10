from typing import Dict, Union, List

import pandas as pd

from code_base.data_calculations.calc_excess_mortality_pop import CalculateEurostatExcessMortalityToPopulation
from code_base.data_output.calc_excess_mortality import CalcExcessMortalityPredicted, CalcEUCountryPop, CalcBGRegionPop
from code_base.data_savers.folder_structure import BaseFolderStructure
from code_base.data_savers.save_file import SaveFile, NameFile
from code_base.data_source.get_source_data import get_source_data
from code_base.data_bindings.data_types import InfostatDataSets, EurostatDataSets


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
    mort_type = EurostatDataSets.MORTALITY_BY_SEX_AGE_REGION
    bg_mort_data = get_source_data(mort_type, analyze_years=years, region='BG')

    pop_type = InfostatDataSets.POP_BY_SEX_AGE_REG
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
    mort_type = EurostatDataSets.MORTALITY_BY_SEX_AGE_COUNTRY
    eu_mort_data = get_source_data(mort_type, analyze_years=years)

    pop_type = EurostatDataSets.POP_BY_SEX_AGE_COUNTRY
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


if __name__ == '__main__':


    age = [
        ['(30-34)', '(35-39)'],
        ['(40-44)', '(45-49)', '(50-54)', '(55-59)', '(60-64)'],
        ['(65-69)'],
    ]
    sex = ['Total', 'Male', 'Female']
    region = 'BG'
    start_week = 10
    years = [2015, 2016, 2017, 2018, 2019, 2020]

    bg_generate_pred_exc_mort(years, age, sex, start_week)
    eu_generate_pred_exc_mort(years, age, sex, start_week)
