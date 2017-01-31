import pandas as pd
import numpy as np

middle_east_countries = ["Yemen People's Republic",'Yemen Arab Republic',\
 'Yemen', 'United Arab Emirates', 'South Sudan',\
 'Sudan', 'Syrian Arab Republic', 'Qatar', 'Saudi Arabia', 'Kuwait', 'Iraq',\
 'Iran, Islamic Republic of', 'Palestine, State of'\
 'Turkey', 'Lebanon', 'Jordan', 'Morocco', 'Algeria', 'Israel', 'Bahrain', 'Oman','Libya', 'Tunisia', 'Egypt', 'Yemen, Rep.'\
 'Iran, Islamic Rep.']

 # WORLD BANK DATA CLEANING

def clean_world_bank_data(indicator):
    '''
    This function cleans any dataset downloaded from the World Bank. This
     function returns a dataframe that applies to the countries of interest,
     drops the unnecessary columns, and reformats the df so it can later be joined
     seamlessly.
     '''
    #drop columns we don't care about
    indicator = indicator.drop(['Country Code', 'Indicator Name', 'Indicator Code'], axis=1)
    #select only countries in the Middle East
    indicator = indicator[indicator['Country Name'].isin(middle_east_countries)]
    #format to later join
    indicator = pd.melt(indicator, id_vars='Country Name')
    #rename columns for uniformity
    indicator.rename(columns={'variable': 'year', 'value': 'indicator'}, inplace=True)
    #converting year column to numeric
    indicator['year'] = indicator['year'].apply(pd.to_numeric)
    #dropping values before 1989
    #indicator = indicator[indicator['year']>1988]
    #dropping values after 2015
    indicator = indicator[indicator['year']<=2015]
    return indicator

# POLITICAL TERROR SCALE DATA CLEANING
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

def missing_pts(country_name, value):
    pts[pts['Country']==country_name]= pts[pts['Country']==country_name].fillna(value)
    return pts[pts['PTS'].isnull()]

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
    return gini


# POLITY: MEASURE OF HOW DEMOCRATIC/AUTOCRATIC A COUNTRY IS (score -10, 10)
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

def missing_values_polity_a(country, value):
    polity[polity['country']==country]= polity[polity['country']=='Lebanon'].fillna(4)
    irq_mean = polity['polity2'][polity['country']=='Iraq'].mean()
    polity[polity['country']=='Iraq']= polity[polity['country']=='Iraq'].fillna(irq_mean)
    polity[polity['country']=='Kuwait']= polity[polity['country']=='Kuwait'].fillna(-10)
    polity[polity['country']=='Syria']= polity[polity['country']=='Syria'].fillna(7)
    return polity

#ETHNICITY
def ethnicity_data_clean(ethnicities):
    '''
    This function takes in a dataframe and returns
    it with the number of ethnicities of a
    country for a given year, dropping unnecessary columns
    and making it specific to middle eastern countries
    '''
    ethnicities= ethnicities[ethnicities['statename'].isin(middle_east_countries)]
    ethnicities = ethnicities.groupby(['statename', 'from', 'to']).count()
    ethnicities = ethnicities.drop(['gwid', 'groupid', 'gwgroupid', 'umbrella', 'size','status', 'reg_aut'], axis=1)
    #still need to create a row for each year//now it's just grouped by country
    return ethnicities

#EMPOWERMENT

def empowerment_cleaning(empowerment):
    '''
    This function takes in a dataframe and returns
    it with the empowerment index of every country for a given year,
    dropping unnecessary columns and making it specific to Middle Eastern countries
    '''
    empowerment = empowerment[empowerment['CTRY'].isin(middle_east_countries)]
    cl_list = ['CTRY', 'YEAR', 'NEW_EMPINX']
    empowerment = empowerment[cl_list]
    empowerment.rename(columns={'YEAR': 'year', 'CTRY': 'country', 'NEW_EMPINX': 'empowerment_indx'}, inplace=True)
    return empowerment

if __name__ == "__main__":
    ## Loading all the DATA
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
    ethnicities = pd.read_excel('data/ethnicities.xls')
    empowerment = pd.read_excel('data/newempinix.xlsx')

    #World Bank Data Cleaning
    youth = clean_world_bank_data(youth)
    youth.rename(columns={'indicator': 'youth'}, inplace=True)
    exports = clean_world_bank_data(unemployment)
    exports.rename(columns={'indicator': 'exports'}, inplace=True)
    unemployment = clean_world_bank_data(unemployment)
    unemployment.rename(columns={'indicator': 'unemployment'}, inplace=True)
    foreign_dir_inv = clean_world_bank_data(foreign_dir_inv)
    foreign_dir_inv.rename(columns={'indicator': 'foreign_dir_inv'}, inplace=True)
    fuel_exports = clean_world_bank_data(fuel_exports)
    fuel_exports.rename(columns={'indicator': 'fuel_exports'}, inplace=True)
    gdppercapita = clean_world_bank_data(gdppercapita)
    gdppercapita.rename(columns={'indicator': 'gdppercapita'}, inplace=True)
    infant_mort = clean_world_bank_data(infant_mort)
    infant_mort.rename(columns={'indicator': 'infant_mort'}, inplace=True)

    #Cleaning Missing Values
    pts = clean_pts(pts)

    #Clean gini
    gini = gini_clean(gini)

    #Clean Polity
    polity = polity_clean(polity)

    #Clean eth dataset
    ethnicities = ethnicity_data_clean(ethnicities)

    #Cleaning Empowerment
    empowerment = empowerment_cleaning(empowerment)

    #Model 1, making missing values = -9999 so the model will ignore
    #independent variables
    new = pd.merge(youth, infant_mort, how='outer', on=['year','Country Name'])
    new2 = pd.merge(new, exports, how='outer', on=['year','Country Name'])
    new3 = pd.merge(new2, fuel_exports, how='outer', on=['year','Country Name'])
    new4 = pd.merge(new3, gdppercapita, how='outer', on=['year','Country Name'])
    new5 = pd.merge(new4, unemployment, how='outer', on=['year','Country Name'])
    new6 = pd.merge(new5, foreign_dir_inv, how='outer', on=['year','Country Name'])
    n = pd.merge(pts, new6, how='outer', on=['year','Country Name'])
    m = pd.merge(n, polity, how='outer', on=['year','Country Name'])
    m.rename(columns={'Country Name': 'country'}, inplace=True)
    al = pd.merge(target, m, how='left', on=['year','country'])
    #dummifying countries
    al = pd.get_dummies(al)
    #missing values = -999999
    al = al.fillna(-999999)
    al.to_csv('al.csv')

    #Model 2 Data Prep- Imputing values
    missing_pts('Bahrain',3)
    missing_pts('Algeria',3)
    missing_pts('Iraq', 5)
    missing_pts('Egypt',3)
    missing_pts('Iran, Islamic Republic of',4)
    missing_pts('Israel', 4)
    missing_pts('Jordan', 3)
    missing_pts('Oman', 2)
    missing_pts('Lebanon',4)
    missing_pts('Morocco', 3)
    missing_pts('Libya', 3)
    missing_pts('Qatar', 2)
    missing_pts('Saudi Arabia', 3)
    missing_pts('South Sudan', 5)
    missing_pts ('Sudan',5)
    missing_pts('Syrian Arab Republic', 5)
    missing_pts('Tunisia', 3)
    missing_pts('Turkey', 4)
    missing_pts('United Arab Emirates', 2)

    polity = missing_values_polity_a(polity)
