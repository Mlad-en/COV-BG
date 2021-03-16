BY_REGION_DECODE_COLUMNS = {
    'Дата': 'Date',
    'BLG_ALL': 'Blagoevgrad',
    'BGS_ALL': 'Burgas',
    'VAR_ALL': 'Varna',
    'VTR_ALL': 'Veliko Tarnovo',
    'VID_ALL': 'Vidin',
    'VRC_ALL': 'Vratsa',
    'GAB_ALL': 'Gabrovo',
    'DOB_ALL': 'Dobrich',
    'KRZ_ALL': 'Kardzhali',
    'KNL_ALL': 'Kyustendil',
    'LOV_ALL': 'Lovech',
    'MON_ALL': 'Montana',
    'PAZ_ALL': 'Pazardzhik',
    'PER_ALL': 'Pernik',
    'PVN_ALL': 'Pleven',
    'PDV_ALL': 'Plovdiv',
    'RAZ_ALL': 'Razgrad',
    'RSE_ALL': 'Ruse',
    'SLS_ALL': 'Silistra',
    'SLV_ALL': 'Sliven',
    'SML_ALL': 'Smolyan',
    'SFO_ALL': 'Sofia',
    'SOF_ALL': 'Sofia (stolitsa)',
    'SZR_ALL': 'Stara Zagora',
    'TGV_ALL': 'Targovishte',
    'HKV_ALL': 'Haskovo',
    'SHU_ALL': 'Shumen',
    'JAM_ALL': 'Yambol',
}

BY_REGION_MELT_VARS = ['Blagoevgrad', 'Burgas', 'Varna', 'Veliko Tarnovo', 'Vidin',
                       'Vratsa', 'Gabrovo', 'Dobrich', 'Kardzhali', 'Kyustendil', 'Lovech',
                       'Montana', 'Pazardzhik', 'Pernik', 'Pleven', 'Plovdiv', 'Razgrad',
                       'Ruse', 'Silistra', 'Sliven', 'Smolyan', 'Sofia', 'Sofia (stolitsa)',
                       'Stara Zagora', 'Targovishte', 'Haskovo', 'Shumen', 'Yambol']

GENERAL_DECODE_COLUMNS = {
    'Дата': 'Date',
    'Направени тестове': 'Tests_Done',
    'Тестове за денонощие': 'Tests_Done_24h',
    'Потвърдени случаи': 'Confirmed_Cases',
    'Активни случаи': 'Active_cases',
    'Нови случаи за денонощие': 'Confirmed_Cases_24h',
    'Хоспитализирани': 'Hospitalized',
    'В интензивно отделение': 'Intensive_Care',
    'Излекувани': 'Recovered',
    'Излекувани за денонощие': 'Recovered_24h',
    'Починали': 'Fatalities',
    'Починали за денонощие': 'Fatalities_24h',
}

RENAME_WEEKLY_COLUMNS = {
            'Tests_Done_24h': 'Tests_week',
            'Confirmed_Cases_24h': 'Confirmed_Cases_Week'
        }