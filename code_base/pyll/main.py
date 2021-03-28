from code_base.pyll.calculate_pyll import CalcExcessMortYLL
from code_base.utils.common_query_params import age_15_64

if __name__ == '__main__':
    c = CalcExcessMortYLL()
    pyll = c.calculate_yll_all_ages()
    c.save_df_to_file(pyll, c.file_location, c.gen_file_name(), method='excel')

    wyll = c.calculate_yll_all_ages(ages=age_15_64, mode='WYLL')
    c.save_df_to_file(wyll, c.file_location, c.gen_file_name(age=age_15_64, mode='WYLL'), method='excel')

    asyr = c.calculate_asyr()
    c.save_df_to_file(asyr, c.file_location, c.gen_file_name(mode='ASYR'), method='excel')