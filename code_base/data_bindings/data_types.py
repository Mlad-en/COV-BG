from enum import Enum, auto


class CoronaVirusBGDataSets(Enum):

    GENERAL = auto()
    BY_REGION = auto()
    BY_AGE_GROUP = auto()
    BY_TEST_TYPE = auto()
    DECEASED_BY_SEX_AGE = auto()
    VACCINATED_INFECTED = auto()
    VACCINATED_HOSPITALIZED = auto()
    VACCINATED_ICU = auto()
    VACCINATED_DECEASED = auto()


class InfostatDataSets(Enum):

    POP_BY_SEX_AGE_REG = auto()
    AVG_LIFE_EXPECTANCY_BY_SEX = auto()
    LIFE_EXPECTANCY_BY_SEX = auto()
    MORTALITY_BY_SEX_AGE_MUN = auto()
    POP_BY_MUNICIPALITY = auto()


class EurostatDataSets(Enum):

    MORTALITY_BY_SEX_AGE_COUNTRY = auto()
    MORTALITY_BY_SEX_AGE_REGION = auto()
    POP_BY_SEX_AGE_COUNTRY = auto()


class WHODataSets(Enum):

    LIFE_EXPECTANCY_BY_AGE_SEX = auto()


class LocalDataSets(Enum):

    UNDATA_Population = auto()
    Italy_Population = auto()
    Covid_Mortality_BG = auto()
    CVD_Europe = auto()

