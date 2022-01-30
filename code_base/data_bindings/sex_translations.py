class SEX_BINDINGS:
    MALE = 'Male'
    FEMALE = 'Female'
    TOTAL = 'Total'


class InfostatBGSexBindings:
    MALE = 'Мъже'
    FEMALE = 'Жени'


EUROSTAT_SEX_CONVERSION = {
    'F': SEX_BINDINGS.FEMALE,
    'M': SEX_BINDINGS.MALE,
    'T': SEX_BINDINGS.TOTAL
}

WHO_SEX_CONVERSION = {
    'MLE':  SEX_BINDINGS.MALE,
    'FMLE': SEX_BINDINGS.FEMALE,
    'BTSX': SEX_BINDINGS.TOTAL
}

UN_DECODE_SEX_GROUPS = {
    'Both Sexes': SEX_BINDINGS.TOTAL,
    'Male':       SEX_BINDINGS.MALE,
    'Female':     SEX_BINDINGS.FEMALE,
}

ITALY_DECODE_SEX_GROUPS = {
    'Totale Maschi':           SEX_BINDINGS.MALE,
    'Totale Maschi e Femmine': SEX_BINDINGS.TOTAL,
    'Totale Femmine':          SEX_BINDINGS.FEMALE

}