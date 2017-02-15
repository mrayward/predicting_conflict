import pandas as pd

middle_east_countries = ["Yemen People's Republic",'Yemen Arab Republic',
 'Yemen', 'Yemen North', 'Yemen South','North Yemen', 'South Yemen', 'United Arab Emirates',
  'South Sudan','Sudan', 'Syrian Arab Republic', 'Qatar', 'Saudi Arabia', 'Kuwait', 'Iraq',
 'Iran, Islamic Republic of', 'Palestine, State of', '(North) Sudan',
 'Turkey', 'Lebanon', 'Jordan', 'Morocco', 'Algeria', 'Israel', 'Bahrain', 'Oman',
 'Libya', 'Tunisia', 'Egypt', 'Yemen, Rep.', 'Iran, Islamic Rep.', 'UAE', 'Yemen (United)', 'Iran']

# consistency in naming
d = {"Yemen (United)": "Yemen", 'UAE':'United Arab Emirates',
'Syrian Arab Republic': 'Syrian', 'Iran, Islamic Rep.': 'Iran',
'Iran, Islamic Republic of': 'Iran', 'Yemen Arab Republic': 'North Yemen',
'Yemen, South':'South Yemen', 'Yemen, Rep.': 'Yemen',
"Yemen People's Republic": 'South Yemen', 'Yemen South': 'South Yemen',
'Yemen North': 'North Yemen'}


def country_name(dataset, dictionary):
    '''
    For every independent variable, this function will bring consistency to the
    naming of countries
    '''
    dataset['Country Name'] = dataset['Country Name'].replace(d)
    return dataset

independence= { 'South Sudan': 2011, 'Algeria': 1962, 'Bahrain': 1971,
            'Egypt': 1922, 'Iraq': 1932, 'Israel': 1948,
            'Jordan': 1946, 'Iran': 1979, 'Kuwait': 1961,
            'Lebanon': 1943, 'Libya': 1951, 'Morocco': 1956,
            'Oman': 1970, 'Qatar': 1971, 'Saudi Arabia': 1932,
            '(North) Sudan': 2011, 'South Sudan': 2011, 'Sudan': 1956,
            'Tunisia': 1956, 'Turkey': 1923, 'United Arab Emirates': 1971,
            'North Yemen': 1962, 'South Yemen': 1967, 'Yemen': 1990}


def country_independence(df, independence):
    '''
    This function ensures no missing values are included for years prior to a
    country's independence
    '''
    for c, i in independence.iteritems():
        country = df[(df['country'] == c) & (df['year'] < i)]
        df = df.drop(country.index)
    return df


# WORLD BANK DATA CLEANING.
def clean_world_bank_data(indicator):
    '''
     Cleans any dataset downloaded from the World Bank. This
     function returns a dataframe that applies to the countries of interest,
     drops the unnecessary columns, and reformats the df so it can later be
     joined seamlessly.
     '''
    # drop columns we don't care about
    indicator = indicator.drop(['Country Code', 'Indicator Name',
                'Indicator Code'], axis=1)
    # select only countries in the Middle East
    indicator = indicator[indicator['Country Name'].isin(middle_east_countries)]
    # format to later join
    indicator = pd.melt(indicator, id_vars='Country Name')
    # rename columns for uniformity
    indicator.rename(columns={'variable': 'year', 'value': 'indicator'}, inplace=True)
    # converting year column to numeric
    indicator['year'] = indicator['year'].apply(pd.to_numeric)
    # dropping values before 1989
    # indicator = indicator[indicator['year']>1988]
    # dropping values after 2015
    indicator = indicator[indicator['year'] <= 2015]
    return indicator


# RENAMING 'INDICATOR' TO SPECIFIC INDICATOR NAME
def rename_wb_indicators(df):
    return df.rename(columns={'indicator': df.name}, inplace=True)


# POLITICAL TERROR SCALE DATA CLEANING
def clean_pts(pts):
    '''
    Cleans the political terror dataset, selecting the max
    value of the pts scores, selecting the relevant countries only, and dropping
    unnecessary columns. This function returns the clean pts dataframe
     '''
    # select only countries in the middle east
    pts = pts[pts['Country'].isin(middle_east_countries)]
    # drop unnecessary columns
    pts = pts.drop(['COW_Code_A', 'COW_Code_N', 'WordBank_Code_A', 'UN_Code_N', 'Region'], axis=1)
    # dataset contains three measures of pts and I am selecting the max value out of the three
    pts['PTS'] = pts['PTS_A']
    pts['PTS'] = pts[['PTS_A', 'PTS_H', 'PTS_S']].apply(max, axis=1)
    # dropping the rest of the irrelevant columns
    pts = pts.drop(['Country_OLD', 'PTS_A', 'PTS_H', 'PTS_S'], axis=1)
    # dropping Palestine because Israel's scores are the same and other
    # datasets don't include it
    pts = pts.drop(pts[pts.Country == 'Palestine, State of'].index)
    # Dropping columns with missing values for South Sudan until the state was
    # officially recognized in 2011
    pts.rename(columns={'Year': 'year'}, inplace=True)
    pts.rename(columns={'Country': 'Country Name'}, inplace=True)
    return pts


# STANDARDIZED INCOME INEQUALITY
def gini_clean(gini):
    """
    This function cleans the standardized income inequality dataset, selecting
    the relevant index, in the relevant countries only, and dropping
    unnecessary columns. This function returns a dataframe with the index_name
    """
    gini = gini[gini['country'].isin(middle_east_countries)]
    col_list = ['country', 'year', 'gini_net']
    gini = gini[col_list]
    gini.rename(columns={'country': 'Country Name'}, inplace=True)
    return gini


# POLITY: MEASURE OF HOW DEMOCRATIC/AUTOCRATIC A COUNTRY IS (score -10, 10)
def polity_clean(polity):
    """
    This function cleans the polity dataset, selecting
    the relevant score, in the relevant countries only, and dropping
    unnecessary columns. This function returns a dataframe with the name.
    """
    polity = polity[polity['country'].isin(middle_east_countries)]
    polity = polity.drop(['democ', 'parcomp', 'autoc', 'polity', 'cyear', 'ccode',
            'scode', 'flag', 'fragment', 'durable', 'xrreg', 'xrcomp',
            'xropen', 'xconst', 'parreg', 'exrec', 'exconst', 'polcomp',
            'prior', 'emonth', 'eday', 'eyear', 'eprec', 'interim', 'bmonth',
            'bday', 'byear', 'bprec', 'post', 'change', 'd4', 'sf',
            'regtrans'], axis=1)
    polity.rename(columns={'country': 'Country Name'}, inplace=True)
    polity = polity[polity['year'] > 1940]
    return polity


def missing_values_polity_a(country, value):
    polity[polity['country'] == country] = polity[polity['country'] == 'Lebanon'].fillna(4)
    irq_mean = polity['polity2'][polity['country'] == 'Iraq'].mean()
    polity[polity['country'] == 'Iraq'] = polity[polity['country'] == 'Iraq'].fillna(irq_mean)
    polity[polity['country'] == 'Kuwait'] = polity[polity['country'] == 'Kuwait'].fillna(-10)
    polity[polity['country'] == 'Syria'] = polity[polity['country'] == 'Syria'].fillna(7)
    return polity


# ETHNICITY
def ethnicity_data_clean(eth):
    '''
    Takes in a dataframe and returns
    it with the number of ethnicities of a
    country for a given year, dropping unnecessary columns
    and making it specific to middle eastern countries
    '''
    eth = eth[eth['COUNTRY'].isin(middle_east_countries)]
    eth.rename(columns={'COUNTRY': 'Country Name', 'ELF85': 'ELF'}, inplace=True)
    col = ['Country Name', 'ELF']
    eth = eth[col]
    return eth


# EMPOWERMENT
def empowerment_cleaning(empowerment):
    '''
    Takes in a dataframe and returns
    it with the empowerment index of every country for a given year,
    dropping unnecessary columns and making it specific to Middle Eastern
    countries
    '''
    empowerment = empowerment[empowerment['CTRY'].isin(middle_east_countries)]
    cl_list = ['CTRY', 'YEAR', 'NEW_EMPINX']
    empowerment = empowerment[cl_list]
    empowerment.rename(columns={'YEAR': 'year', 'CTRY': 'Country Name', 'NEW_EMPINX':
        'empowerment_indx'}, inplace=True)
    return empowerment

if __name__ == "__main__":
    # Loading all the DATA
    youth = pd.read_excel('data/youth.xls')
    exports = pd.read_excel('data/exports.xls')
    unemployment = pd.read_excel('data/unemployment.xls')
    foreign_dir_inv = pd.read_excel('data/for_dir_inv.xls')
    fuel_exports = pd.read_excel('data/fuel.xls')
    gdppercapita = pd.read_excel('data/gdppercapita.xls')
    infant_mort = pd.read_excel('data/infmort.xls')
    pts = pd.read_excel('data/PoliticalTerrorScale.xlsx')
    gini = pd.io.stata.read_stata('data/SWIIDv5_0.dta')
    polity = pd.read_excel('data/polity.xls')
    empowerment = pd.read_excel('data/newempinix.xlsx')
    eth = pd.read_excel('data/elf.xls')
    target = pd.read_csv('data/target.csv')

    # World Bank Data Cleaning
    youth = clean_world_bank_data(youth)
    exports = clean_world_bank_data(unemployment)
    unemployment = clean_world_bank_data(unemployment)
    foreign_dir_inv = clean_world_bank_data(foreign_dir_inv)
    fuel_exports = clean_world_bank_data(fuel_exports)
    gdppercapita = clean_world_bank_data(gdppercapita)
    infant_mort = clean_world_bank_data(infant_mort)

    # Assigning names to the dataframes
    youth.name = 'youth'
    exports.name = 'exports'
    unemployment.name = 'uneployment'
    foreign_dir_inv.name = 'foreign_dir_inv'
    fuel_exports.name = 'fuel_exports'
    gdppercapita.name = 'gdppercapita'
    infant_mort.name = 'infant_mort'

    # making list of df names of indicators
    wb_df = [youth, exports, unemployment, foreign_dir_inv, fuel_exports,
                gdppercapita, infant_mort]

    list_of_df = [youth, exports, unemployment, foreign_dir_inv, fuel_exports,
                gdppercapita, infant_mort, pts, gini, polity, eth, empowerment]

    # Renaming generic 'indicator' column to the actual name of the indicator
    for df in wb_df:
        rename_wb_indicators(df)

    # Cleaning Missing Values
    pts = clean_pts(pts)
    pts.name = 'pts'

    # Clean gini
    gini = gini_clean(gini)
    gini.name = 'gini'

    # Clean Polity
    polity = polity_clean(polity)
    polity.name = 'polity'

    # Clean eth dataset
    eth = ethnicity_data_clean(eth)
    eth.name = 'eth'

    # Cleaning Empowerment
    empowerment = empowerment_cleaning(empowerment)
    empowerment.name = 'empowerment'

    # Steamlining country names
    youth = country_name(youth, d)
    exports = country_name(exports, d)
    fuel_exports = country_name(fuel_exports, d)
    gdppercapita = country_name(gdppercapita, d)
    foreign_dir_inv = country_name(foreign_dir_inv, d)
    infant_mort = country_name(infant_mort, d)
    unemployment = country_name(unemployment, d)
    pts = country_name(pts, d)
    polity = country_name(polity, d)
    gini = country_name(gini, d)
    empowerment = country_name(empowerment, d)
    eth = country_name(eth, d)

    # Cleaning target
    target = target.drop('Unnamed: 0', axis=1)

    # Saving Clean Dfs to csvs for feature engineering manipulation
    youth.to_csv('youth.csv')
    unemployment.to_csv('unemployment.csv')
    exports.to_csv('exports.csv')
    fuel_exports.to_csv('fuel_exports.csv')
    gdppercapita.to_csv('gdppercapita.csv')
    infant_mort.to_csv('infant_mort.csv')
    pts.to_csv('pts.csv')
    polity.to_csv('polity.csv')
    gini.to_csv('gini.csv')
    empowerment.to_csv('empowerment.csv')
    eth.to_csv('eth.csv')
    foreign_dir_inv.to_csv('foreign_dir_inv.csv')
    target.to_csv('target.csv')
