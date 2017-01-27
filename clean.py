import pandas as pd
import numpy as np

middle_east_countries = ["Yemen People's Republic",'Yemen Arab Republic',\
 'Yemen', 'United Arab Emirates', 'South Sudan',\
 'Sudan', 'Syrian Arab Republic', 'Qatar', 'Saudi Arabia', 'Kuwait', 'Iraq',\
 'Iran, Islamic Republic of', 'Palestine, State of'\
 'Turkey', 'Lebanon', 'Jordan', 'Morocco', 'Algeria', 'Israel', 'Bahrain', 'Oman','Libya', 'Tunisia', 'Egypt', 'Yemen, Rep.'\
 'Iran, Islamic Rep.']

 # WORLD BANK DATA CLEANING
indicator1 = pd.read_excel('youth.xls')
indicator2 = pd.read_excel('exports.xls')
indicator3 = pd.read_excel('unemployment.xls')
indicator4 = pd.read_excel('for_dir_inv.xls')
indicator5 = pd.read_excel('fuel.xls')
indicator6 = pd.read_excel('gdppercapita.xls')
indicator7 = pd.read_excel('infmort.xls')
indicator8 = pd.read_excel('accountability.xls')

 def clean_world_bank_data(indicator):
     """
     This function cleans any dataset downloaded from the World Bank. This
     function returns a dataframe that applies to the countries of interest,
     drops the unnecessary columns, and reformats the df so it can later be joined
     seamlessly.
     """
    #drop columns we don't care about
    indicator = indicator.drop(['Country Code', 'Indicator Name', 'Indicator Code'], axis =1)
    #select only countries in the Middle East
    indicator = indicator[indicator['Country Name'].isin(middle_east_countries)]
    #format to later join
    indicator = pd.melt(indicator, id_vars='Country Name')
    #rename columns for uniformity
    indicator.rename(columns={'variable': 'year', 'value': 'indicator'}, inplace=True)
    #converting year column to numeric
    indicator['year'] = indicator['year'].apply(pd.to_numeric)
    #dropping values before 1989
    indicator = indicator[indicator['year']>1988]
    #dropping values after 2015
    indicator = indicator[indicator['year']<=2015]
    return indicator

# POLITICAL TERROR SCALE DATA CLEANING
pts = pd.read_excel('PoliticalTerrorScale.xlsx')

def clean_pts(pts):
    """
    This function cleans the political terror dataset, selecting the max
    value of the pts scores, selecting the relevant countries only, and dropping
    unnecessary columns. This function returns the clean pts dataframe
    """
    #select only countries in the middle east
    pts = pts[pts['Country'].isin(middle_east_countries)]
    #drop unnecessary columns
    pts = pts.drop(['COW_Code_A', 'COW_Code_N','WordBank_Code_A', 'UN_Code_N', 'Region'], axis =1)
    #dataset contains three measures of pts and I am selecting the max value out of the three
    pts['PTS'] = pts['PTS_A']
    pts['PTS']= pts[['PTS_A', 'PTS_H', 'PTS_S']].apply(max, axis=1)
    #dropping the rest of the irrelevant columns
    pts= pts.drop(['Country_OLD', 'PTS_A', 'PTS_H', 'PTS_S'], axis=1)
    #dropping Palestine because Israel's scores are the same and other datasets
    #don't include it
    pts = pts.drop(pts[pts.Country == 'Palestine, State of'].index)
    ## Dropping columns with missing values for South Sudan until the state was
    ##officially recognized in 2011
    ssudan = pts[(pts['Country']=='South Sudan')&(pts['Year']<2011)]
    pts = pts.drop(ssudan.index)
    ##Yemen had different nanes at different points in time- this is to homogenize it
    dic = {"Yemen People's Republic": 'Yemen', 'Yemen Arab Republic':'Yemen'}
    pts['Country'] = pts['Country'].replace(dic)

    return pts

def missing(country_name, value):
    pts[pts['Country']==country_name]= pts[pts['Country']==country_name].fillna(value)
    return pts[pts['PTS'].isnull()]

missing('Israel', 4)
missing('Jordan', 3)
missing('Oman', 2)
missing('Lebanon',3)
missing('Morocco', 3)
missing('Libya', 3)
missing('Qatar', 2)

# STANDARDIZED INCOME INEQUALITY
gini = pd.io.stata.read_stata('SWIIDv5_0.dta')
def gini_clean(gini):
    """
    This function cleans the standardized income inequality dataset, selecting
    the relevant index, in the relevant countries only, and dropping
    unnecessary columns. This function returns a dataframe with the index_name
    """
    gini = gini[gini['country'].isin(middle_east_countries)]
    col_list = ['country', 'year', 'gini_net']
    gini = gini[col_list]
    return gini


# POLITY: MEASURE OF HOW DEMOCRATIC/AUTOCRATIC A COUNTRY IS (score -10, 10)
polity = pd.read_excel('polity.xls')
def polity_clean(polity):
    """
    This function cleans the polity dataset, selecting
    the relevant score, in the relevant countries only, and dropping
    unnecessary columns. This function returns a dataframe with the name.
    """
    polity = polity[polity['country'].isin(middle_east_countries)]
    polity = polity.drop(['democ','parcomp', 'autoc','polity','cyear', 'ccode','scode', 'flag', 'fragment', 'durable', 'xrreg','xrcomp', 'xropen', 'xconst', 'parreg', 'exrec', 'exconst', 'polcomp', 'prior', 'emonth', 'eday', 'eyear', 'eprec', 'interim', 'bmonth', 'bday', 'byear', 'bprec', 'post', 'change', 'd4', 'sf', 'regtrans'], axis =1)
    polity = polity[polity['year']>1940]
    return polity

def missing_values_polity_a(polity):
    polity[polity['country']=='Lebanon']= polity[polity['country']=='Lebanon'].fillna(4)
    irq_mean = polity['polity2'][polity['country']=='Iraq'].mean()
    polity[polity['country']=='Iraq']= polity[polity['country']=='Iraq'].fillna(irq_mean)
    polity[polity['country']=='Kuwait']= polity[polity['country']=='Kuwait'].fillna(-10)
    polity[polity['country']=='Syria']= polity[polity['country']=='Syria'].fillna(7)
    return polity

#ETHNICITY
ethnicities = pd.read_excel('ethnicities.xls')
def ethnicity_data_clean(indicatr):
    '''
    This function takes in a dataframe and returns
    it with the number of ethnicities of a
    country for a given year, dropping unnecessary columns
    and making it specific to middle eastern countries
    '''
    indicatr= indicatr[indicatr['statename'].isin(middle_east_countries)]
    indicatr = indicatr.groupby(['statename', 'from', 'to']).count()
    indicatr = indicatr.drop(['gwid', 'groupid', 'gwgroupid', 'umbrella', 'size','status', 'reg_aut'], axis=1)
    #still need to create a row for each year//now it's just grouped by country
    return ethnicities

    indicatr = ethnicities

#EMPOWERMENT
empowerment = pd.read_excel('newempinix.xlsx')

def empowerment_cleaning(empowerment):
    '''
    This function takes in a dataframe and returns
    it with the empowerment index of every country for a given year,
    dropping unnecessary columns and making it specific to Middle Eastern countries
    '''
    empowerment = pd.read_excel(d)
    empowerment = empowerment[empowerment['CTRY'].isin(middle_east_countries)]
    cl_list = ['CTRY', 'YEAR', 'NEW_EMPINX']
    empowerment = empowerment[cl_list]
    empowerment.rename(columns={'YEAR': 'year', 'CTRY': 'country', 'NEW_EMPINX': 'empowerment_indx'}, inplace=True)
    return empowerment
