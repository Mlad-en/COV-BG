from code_base.pyll.calculate_pyll import CalcExcessMortPyll
from code_base.utils.common_query_params import age_15_64

if __name__ == '__main__':
    c = CalcExcessMortPyll()
    pyll = c.calculate_yll_all_ages()
    c.save_df_to_file(pyll, c.file_location, c.gen_file_name(), method='excel')
    yppll = c.calculate_yll_all_ages(ages=age_15_64, mode='YPPLL')
    c.save_df_to_file(yppll, c.file_location, c.gen_file_name(age=age_15_64, mode='YPPLL'), method='excel')