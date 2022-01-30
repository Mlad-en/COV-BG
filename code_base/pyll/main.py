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
    date_ranges = [
        {'start_date': (2020, 3, 1),
         'end_date': (2020, 12, 31)},
        {'start_date': (2021, 1, 1),
         'end_date': (2021, 7, 6)},
        {'start_date': (2020, 3, 1),
         'end_date': (2021, 5, 18)},
    ]

    for date_range in date_ranges:
        cz = MergeMortalityLifeExpectancy('Czechia')
        cz.calc_full_yll(start_date=date_range['start_date'], end_date=date_range['end_date'])
        bg = MergeMortalityLifeExpectancy('Bulgaria')
        bg.calc_full_yll(sheet_name='Covid_19_combined_without_unk', start_date=date_range['start_date'], end_date=date_range['end_date'])
        # Generate datasets for the 40-64 age groups for Czechia and Bulgaria.
        cz.calc_full_yll(start_age=40, end_age=64, start_date=date_range['start_date'], end_date=date_range['end_date'])
        bg.calc_full_yll(start_age=40, end_age=64, sheet_name='Covid_19_combined_without_unk', start_date=date_range['start_date'], end_date=date_range['end_date'])
        # Calculate WYLL for Bulgaria and Czechia, assuming a cut-off age of 65.
        bg.calc_full_yll(sheet_name='Covid_19_combined_without_unk', mode='WYLL', start_date=date_range['start_date'], end_date=date_range['end_date'])
        cz.calc_full_yll(mode='WYLL', start_date=date_range['start_date'], end_date=date_range['end_date'])