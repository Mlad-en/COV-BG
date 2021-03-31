from code_base.pyll.calc_full_pyll import MergeMortalityLifeExpectancy
from code_base.pyll.calculate_pyll import CalcExcessMortYLL
from code_base.utils.common_query_params import age_15_64, ages_all

if __name__ == '__main__':
    # Calculate PYLL and ASYR without 90+ age group
    c = CalcExcessMortYLL()
    pyll = c.calculate_yll_all_ages()
    c.save_df_to_file(pyll, c.file_location, c.gen_file_name(), method='excel')
    wyll = c.calculate_yll_all_ages(ages=age_15_64, mode='WYLL')
    c.save_df_to_file(wyll, c.file_location, c.gen_file_name(age=age_15_64, mode='WYLL'), method='excel')
    asyr = c.calculate_asyr()
    c.save_df_to_file(asyr, c.file_location, c.gen_file_name(mode='ASYR'), method='excel')

    # Calculate PYLL and ASYR with 90+ age group with data for 85+ provided by the WHO
    c = CalcExcessMortYLL(over_90_included=True)
    pyll = c.calculate_yll_all_ages(ages=ages_all)
    c.save_df_to_file(pyll, c.file_location, c.gen_file_name(), method='excel')
    asyr = c.calculate_asyr(ages=ages_all)
    c.save_df_to_file(asyr, c.file_location, c.gen_file_name(mode='ASYR'), method='excel')

    # Calculate PYLL and ASYR with 90+ age group with static life expectancy data for 90+ (4 years; hard-coded)
    c = CalcExcessMortYLL(over_90_included=True, static_lf_over_90=True)
    pyll = c.calculate_yll_all_ages(ages=ages_all)
    c.save_df_to_file(pyll, c.file_location, c.gen_file_name(more_info='_static_over_90'), method='excel')
    asyr = c.calculate_asyr(ages=ages_all)
    c.save_df_to_file(asyr, c.file_location, c.gen_file_name(mode='ASYR', more_info='_static_over_90'), method='excel')

    # Calculate Full Covid-19 Mortality PYLL - Czechia and Bulgaria.
    cz = MergeMortalityLifeExpectancy('Czechia')
    cz.calc_full_pyll()
    bg = MergeMortalityLifeExpectancy('Bulgaria')
    bg.calc_full_pyll(sheet_name='combined_without_unk')
    # Generate datasets for the 40-64 age groups for Czechia and Bulgaria.
    cz.calc_full_pyll(start_age=40, end_age=64)
    bg.calc_full_pyll(start_age=40, end_age=64, sheet_name='combined_without_unk')