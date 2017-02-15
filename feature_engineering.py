import pandas as pd


country_name_list = ['Algeria', 'Bahrain', 'United Arab Emirates', 'Iran',
            'Iraq', 'Kuwait', 'Yemen', 'Oman', 'Qatar', 'Egypt', 'Sudan',
            'South Sudan', 'Syria', 'Jordan', 'Morocco', 'Saudi Arabia',
            'South Yemen', 'North Yemen', 'Israel', 'Libya', 'Tunisia',
            'Turkey', 'Lebanon']


def create_columns(df):
    df[df.name+'_this_year'] = df[df.name]
    return df

def youth_update(df, country_name):
    country = df[df['Country Name']== country_name]
    country[df.name] = country[df.name].shift()
    country[df.name+'_difference_year_before']= country[df.name+'_this_year'] - country[df.name]
    country.drop(df.name, axis=1, inplace=True)
    return country

def updates_by_country(df):
    algeria = youth_update(df, 'Algeria')
    bahrain = youth_update(df, 'Bahrain')
    uae = youth_update(df, 'United Arab Emirates')
    iraq = youth_update(df, 'Iraq')
    iran = youth_update(df, 'Iran')
    kuwait = youth_update(df, 'Kuwait')
    yemen = youth_update(df, 'Yemen')
    oman = youth_update(df, 'Oman')
    qatar = youth_update(df, 'Qatar')
    egypt = youth_update(df, 'Egypt')
    sudan = youth_update(df, 'Sudan')
    ssudan = youth_update(df, 'South Sudan')
    syria = youth_update(df, 'Syria')
    jordan = youth_update(df, 'Jordan')
    morocco = youth_update(df, 'Morocco')
    saudi = youth_update(df, 'Saudi Arabia')
    syemen = youth_update(df, 'South Yemen')
    nyemen = youth_update(df, 'North Yemen')
    israel = youth_update(df, 'Israel')
    libya = youth_update(df, 'Libya')
    tunisia = youth_update(df, 'Tunisia')
    turkey = youth_update(df, 'Turkey')
    lebanon = youth_update(df, 'Lebanon')
    all_df = algeria.append(bahrain)
    countries = [uae, iraq, iran, kuwait, yemen, oman, qatar, egypt, sudan, ssudan, syria, jordan, morocco, saudi, syemen, nyemen, israel, libya, tunisia, lebanon, turkey]
    for country in countries:
        all_df = all_df.append(country)
    return all_df

# Define function to merge all datasets into one
def merge_datasets(df1, df2):
    unite = pd.merge(df1, df2, how='outer', on=['year', 'Country Name'])
    return unite

# Defining left join function
def left_join(left, right):
    everyone = pd.merge(left, right, how='left', on=['year', 'country'])
    return everyone


# Defining function to fill missing values
def fill_missing_values(df):
    df = df.fillna(-999999)
    return df


if __name__ == "__main__":
    # Loading all the clean data
    youth = pd.read_csv('youth.csv')
    exports = pd.read_csv('exports.csv')
    unemployment = pd.read_csv('unemployment.csv')
    foreign_dir_inv = pd.read_csv('foreign_dir_inv.csv')
    fuel_exports = pd.read_csv('fuel_exports.csv')
    gdppercapita = pd.read_csv('gdppercapita.csv')
    infant_mort = pd.read_csv('infant_mort.csv')
    pts = pd.read_csv('pts.csv')
    gini = pd.read_csv('gini.csv')
    polity = pd.read_csv('polity.csv')
    empowerment = pd.read_csv('empowerment.csv')
    eth = pd.read_csv('eth.csv')
    target = pd.read_csv('target.csv')

    # Assigning names to the dataframes
    youth.name = 'youth'
    exports.name = 'exports'
    unemployment.name = 'uneployment'
    foreign_dir_inv.name = 'foreign_dir_inv'
    fuel_exports.name = 'fuel_exports'
    gdppercapita.name = 'gdppercapita'
    infant_mort.name = 'infant_mort'
    pts.name = 'pts'
    gini.name = 'gini'
    polity.name = 'polity'
    eth.name = 'eth'
    empowerment.name = 'empowerment'

    # # Defining countries
    # countries = [uae, iraq, iran, kuwait, yemen, oman, qatar, egypt, sudan,
    #     ssudan, syria, jordan, morocco, saudi, syemen, nyemen, israel, libya,
    #     tunisia, lebanon, turkey]

    # Creating Columns with Previous year values and difference in values
    youth = create_columns(youth)
    all_youth = updates_by_country(youth)

    unemployment = create_columns(unemployment)
    all_unemployment = updates_by_country(unemployment)

    foreign_dir_inv = create_columns(foreign_dir_inv)
    all_foreign_dir_inv = updates_by_country(foreign_dir_inv)

    fuel_exports = create_columns(fuel_exports)
    all_fuel_exports = updates_by_country(fuel_exports)

    empowerment = create_columns(empowerment)
    all_empowerment = updates_by_country(empowerment)

    gdppercapita = create_columns(gdppercapita)
    all_gdppercapita = updates_by_country(gdppercapita)

    pts = create_columns(pts)
    all_pts = updates_by_country(pts)

    polity = create_columns(polity)
    all_polity = updates_by_country(polity)

    gini = create_columns(gini)
    all_gini = updates_by_country(gini)

    eth = create_columns(eth)
    all_eth = updates_by_country(eth)

    infant_mort = create_columns(infant_mort)
    all_infant_mort = updates_by_country(infant_mort)

    exports = create_columns(exports)
    all_exports = updates_by_country(exports)


    # Merging all dataframes into one
    united1 = merge_datasets(all_youth, all_unemployment)
    united2 = merge_datasets(united1, all_exports)
    united3 = merge_datasets(united2, all_eth)
    united4 = merge_datasets(united3, all_gdppercapita)
    united5 = merge_datasets(united4, all_gini)
    united6 = merge_datasets(united5, all_fuel_exports)
    united7 = merge_datasets(united6, all_empowerment)
    united8 = merge_datasets(united7, all_pts)
    united9 = merge_datasets(united8, all_polity)
    united10 = merge_datasets(united9, all_infant_mort)
    united11 = merge_datasets(united10, all_fuel_exports)

    # m.rename(columns={'Country Name': 'country'}, inplace=True)
    # al = pd.merge(target, m, how='left', on=['year', 'country'])
    #
    # al.to_csv('al.csv')
