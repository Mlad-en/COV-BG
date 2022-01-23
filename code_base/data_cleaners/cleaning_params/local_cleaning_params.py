from code_base.data_bindings.column_naming_consts import COLUMN_HEADING_CONSTS
from code_base.data_bindings.sex_translations import SEX_BINDINGS


class UnDataHeaders:
    LOCATION_PRE = 'Country or Area'
    POPULATION_PRE = 'Value'
    AREA = 'Area'
    SEX = COLUMN_HEADING_CONSTS.SEX
    AGE = COLUMN_HEADING_CONSTS.AGE


class ItalyPopDataHeaders:

    MEN = 'Totale Maschi'
    WOMEN = 'Totale Femmine'
    TOTAL = 'Totale Maschi e Femmine'
    AGE = 'Eta'

    Translate_MEN = SEX_BINDINGS.MALE
    TRANSLATE_WOMEN = SEX_BINDINGS.FEMALE
    TRANSLATE_TOTAL = SEX_BINDINGS.TOTAL
    TRANSLATE_SEX = COLUMN_HEADING_CONSTS.SEX
    TRANSLATE_AGE = COLUMN_HEADING_CONSTS.AGE
    POPULATION = COLUMN_HEADING_CONSTS.POPULATION
    LOCATION = COLUMN_HEADING_CONSTS.LOCATION


class CVDsEuropeHeaders:

    Translate_Location = 'Unnamed: 2'
    Translate_Deaths_Raw = 'Unnamed: 3'
    Translate_Share_Total = 'Unnamed: 4'
    Translate_Share_Men = 'Unnamed: 5'
    Translate_Share_Women = 'Unnamed: 6'
    Translate_Standardized_Total = 'Unnamed: 7'
    Translate_Standardized_Men = 'Unnamed: 8'
    Translate_Standardized_Women = 'Unnamed: 9'
    Translate_Standardized_LT65 = 'Unnamed: 10'
    Translate_Standardized_GTE65 = 'Unnamed: 11'

    Location = COLUMN_HEADING_CONSTS.LOCATION
    Deaths_Raw = 'Number of deaths'
    Share_Total = 'Share of deaths-Total'
    Share_Men = 'Share of deaths-Males'
    Share_Women = 'Share of deaths-Females'
    Standardized_total = 'Per 100_000-Total'
    Standardized_Men = 'Per 100_000-Male'
    Standardized_Women = 'Per 100_000-Females'
    Standardized_LT65 = 'Per 100_000-LT65'
    Standardized_GTE65 = 'Per 100_000-GTE65'

