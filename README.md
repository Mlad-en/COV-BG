# COV-BG

## About the project

The current project is used to analyze publicly-available data regarding the Covid-19 pandemic in Europe, and especially in Bulgaria (by NUT-3 regions).


## Datasets used

The following publicly available datasets were used for this analysis:

1. **Eurostat Datasets**
   
   1.1. "[Deaths by week, sex and 5-year age group](https://appsso.eurostat.ec.europa.eu/nui/show.do?dataset=demo_r_mwk_05&lang=en)" - Dataset contains information about EU countries partitioned by sex (Female, Male, Total) and by age groups (increments of 5).
   
   This dataset was used to calculate the excess mortality and [P-scores](https://ourworldindata.org/excess-mortality-covid#excess-mortality-p-scores) values for EU countries.

   1.2. "[Deaths by week, sex, 5-year age group and NUTS 3 region](https://appsso.eurostat.ec.europa.eu/nui/show.do?dataset=demo_r_mweek3)" - Dataset contains information about EU [NUTS-3 regions](https://ec.europa.eu/eurostat/web/nuts/background) partitioned by sex (Female, Male, Total) and by age groups (increments of 5).
   
   This dataset was used to calculate excess mortality and P-scores for **Bulgarian** regions.

    1.3. "[Population on 1 January by age group and sex](https://appsso.eurostat.ec.europa.eu/nui/show.do?dataset=demo_pjangroup&lang=en)" - Dataset contains information about EU countries' population partitioned by sex (Female, Male, Total) and by age groups (increments of 5).
    
    This dataset was used to normalize excess mortality per 100,000 people for EU countries. It was also used to calculate the Potential Years of Life Lost (PYLL) and [Age-Standardized Year Of Life Lost Rate](https://academic.oup.com/ije/article/48/4/1367/5281229#140004792) (ASYR).

2. **Infostat Datasets**

    2.1. "[POPULATION BY DISTRICTS, AGE, PLACE OF RESIDENCE AND SEX](https://infostat.nsi.bg/infostat/pages/reports/query.jsf?x_2=1168)" - Dataset contains information about Bulgarian region's population partitioned by sex (Female, Male, Total) and by age groups (increments of 5).
    
    This dataset was used to normalize excess mortality per 100,000 people for Bulgarian regions. It was also used to calculate total PYLL for different regions in Bulgaria.

3. **CoronaVirus.bg**

    3.1. "[General distribution statistics](https://data.egov.bg/data/resourceView/e59f95dd-afde-43af-83c8-ea2916badd19)" - Dataset contains daily general information about the Covid-19 pandemic within Bulgaria.
    
    This dataset was used to compare the official Covid-19 deaths to excess mortality on a weekly basis in Bulgaria. This allows for a quick overview of the under-count of mortality due to the pandemic.

4. **World Health Organization**

    4.1. "[Expectation of life at age x](https://apps.who.int/gho/athena/data/GHO/LIFE_0000000035.csv?filter=REGION:EUR;YEAR:2019)" - dataset contains life expectancy per country in Europe partitioned by sex (Female, Male, Total) and age groups (increments of 5).
    
    This dataset was used to calculate the per-age-group years of life lost. These were required for calculating PYLL, ASYR and [Working Years of Life Lost](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/574053/alcohol_public_health_burden_statistics.pdf) (WYLL).

5. **United Nations**

    5.1.[Population by age, sex and urban/rural residence](https://data.un.org/Data.aspx?d=POP&f=tableCode%3A22) - Dataset contains information about EU countries' population partitioned by sex (Female, Male, Total) and by age groups (increments of 5). 

    Dataset is used to supplement Eurostat's [Population on 1 January by age group and sex](https://appsso.eurostat.ec.europa.eu/nui/show.do?dataset=demo_pjangroup&lang=en) dataset. The Eurostat Population dataset goes up to age group 85+, while its mortality dataset goes up to 90+. To desegregate the data for age groups 85-89 and 90+ population metrics have been pulled from the UN dataset.

6. **Italian Statistical Office**

    6.1. [Resident population by age, sex and marital status on 1st January 2020](https://demo.istat.it/popres/index.php?anno=2020&lingua=eng) - data contains population metrics for Italy. 
    Used to supplement for Italy for age groups 85-89 and 90+.

7. **Federal Health Monitoring**

    7.1. [Standard populations used for age standardization in the information system of the Federal Health Monitoring](https://www.gbe-bund.de/gbe/pkg_olap_tables.prc_set_hierlevel?p_uid=gast&p_aid=7584310&p_sprache=E&p_help=2&p_indnr=1000&p_ansnr=76943455&p_version=2&p_dim=D.002&p_dw=40&p_direction=drill) - dataset contains a standardized population across european countries (Standard population of Europe 2013).

    Dataset used to calculate ASYR by standardizing EU populations by age group across countries.