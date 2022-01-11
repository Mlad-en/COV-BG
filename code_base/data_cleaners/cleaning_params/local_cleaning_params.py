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
    LIFE_EXPECTANCY = COLUMN_HEADING_CONSTS.LIFE_EXPECTANCY
