#!/usr/bin/env python
# coding: utf-8

# In[66]:


import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


# In[67]:


# Code for simplifying the piece where the year must be added to all dataframes
# Current approach: for loop to import and name all dataframes with a line that adds a year column to each
#timespan = [2022,2021,2020,2019,2018,2017,2016,2015,2014,2013,2012,2011,2010,2009,2008,2007,2006,2005,2004]
#pricedf_list = {}
#for year in timespan:
    #pricedf_list[] = 
    
# Refer to advanced OOP class for this


# In[68]:


# Reading in price data. Each year contained in a different file. p2022 = Price data for 2022
p2022 = pd.read_csv('./Data-CSV/Price2022.csv')
p2021 = pd.read_csv('./Data-CSV/Price2021.csv')
p2020 = pd.read_csv('./Data-CSV/Price2020.csv')
p2019 = pd.read_csv('./Data-CSV/Price2019.csv')
p2018 = pd.read_csv('./Data-CSV/Price2018.csv')
p2017 = pd.read_csv('./Data-CSV/Price2017.csv')
p2016 = pd.read_csv('./Data-CSV/Price2016.csv')
p2015 = pd.read_csv('./Data-CSV/Price2015.csv')
p2014 = pd.read_csv('./Data-CSV/Price2014.csv')
p2013 = pd.read_csv('./Data-CSV/Price2013.csv')
p2012 = pd.read_csv('./Data-CSV/Price2012.csv')
p2011 = pd.read_csv('./Data-CSV/Price2011.csv')
p2010 = pd.read_csv('./Data-CSV/Price2010.csv')
p2009 = pd.read_csv('./Data-CSV/Price2009.csv')
p2008 = pd.read_csv('./Data-CSV/Price2008.csv')
p2007 = pd.read_csv('./Data-CSV/Price2007.csv')
p2006 = pd.read_csv('./Data-CSV/Price2006.csv')
p2005 = pd.read_csv('./Data-CSV/Price2005.csv')
p2004 = pd.read_csv('./Data-CSV/Price2004.csv')

# 2003 data is price (cents per kWh) by individual utility company by consumer type
# 2002 data has a mean price for each state
# Handling separately due to significantly different structure
p2003Res = pd.read_csv('./Data-CSV/Price2003_Res.csv')
p2003Com = pd.read_csv('./Data-CSV/Price2003_Com.csv')
p2003Ind = pd.read_csv('./Data-CSV/Price2003_Ind.csv')
p2002Res = pd.read_csv('./Data-CSV/Price2002_Res.csv')
p2002Com = pd.read_csv('./Data-CSV/Price2002_Com.csv')
p2002Ind = pd.read_csv('./Data-CSV/Price2002_Ind.csv')

# 2001 - 1994 data is contained in pdf format, must be converted to csv and structured individually for consistency
p2001 = pd.read_csv("./Data-CSV/Price2001.csv", encoding = 'latin1')
p2000 = pd.read_csv('./Data-CSV/Price2000.csv', encoding = 'latin1')
p1999 = pd.read_csv('./Data-CSV/Price1999.csv', encoding = 'latin1')
p1998 = pd.read_csv('./Data-CSV/Price1998.csv', encoding = 'latin1')
p1997 = pd.read_csv('./Data-CSV/Price1997.csv', encoding = 'latin1')
p1996 = pd.read_csv('./Data-CSV/Price1996.csv', encoding = 'latin1')
p1995 = pd.read_csv('./Data-CSV/Price1995.csv', encoding = 'latin1')
p1994 = pd.read_csv('./Data-CSV/Price1994.csv', encoding = 'latin1')

dfs = [p2022, p2021, p2020, p2019, p2018, p2017, p2016, p2015, p2014, p2013, 
       p2012, p2011, p2010, p2009, p2008, p2007, p2006, p2005, p2004]
dfs2003 = [p2003Res, p2003Ind, p2003Com]
dfs2002 = [p2002Res, p2002Com, p2002Ind]

state_prices = {}
state_pricing = {}

# Should enter as df for simplicity (Year could be key and have two values - headline and core)
# Including both headline and core inflation data. Price is adjusted according to headline while core is used as independent variable
# Headline inflation rates (Minneapolis Fed - https://www.minneapolisfed.org/about-us/monetary-policy/inflation-calculator/consumer-price-index-1913-)
headline_inflation = [2.8,2.9,2.3,1.6,2.2,3.4,2.8,1.6,2.3,2.7,3.4,3.2,2.9,3.8,-0.4,1.6,3.2,2.1,1.5,1.6,0.1,1.3,2.1,2.4,1.8,1.2,4.7,8.0]
headline_cpi = [100]
for x in headline_inflation:
    headline_cpi.append(round(((x / 100)+1) * headline_cpi[-1], 4))
    
# Core inflation rates (USInflationCalculator - https://www.usinflationcalculator.com/inflation/united-states-core-inflation-rates/)
inflation_rates = [3, 2.6, 2.2, 2.4, 1.9, 2.6, 2.7, 1.9, 1.1, 2.2, 2.2, 2.6, 2.4, 1.8, 1.8, 0.8, 2.2, 1.9, 1.7, 1.6, 2.1, 2.2, 1.8, 2.2, 2.3, 1.6, 5.5, 5.7]
core_cpi = [100]
for x in inflation_rates:
    core_cpi.append(round(((x / 100)+1) * core_cpi[-1], 4))

# Creating df to concatenate with 94 - 01 price data
headcpi_df = pd.DataFrame(headline_cpi)
headcpi_df.rename(columns={0:'CPI'}, inplace = True)
cpi_df = pd.DataFrame(core_cpi)
cpi_df.rename(columns={0:'Core_CPI'}, inplace = True)
timespan = ['2022','2021','2020','2019','2018','2017','2016','2015','2014','2013','2012','2011','2010','2009','2008',
            '2007','2006','2005','2004', '2003', '2002', '2001', '2000', '1999', '1998', '1997', '1996', '1995', '1994']
headcpi_df['Year'] = timespan[::-1]
cpi_df['Year'] = timespan[::-1]
headcpi_df.set_index('Year', inplace = True)
cpi_df.set_index('Year', inplace = True)

# Creating dictionary and list of key values for changing full state names to abbreviated
abbrev_dict = {
               "Alabama": "AL","Alaska": "AK","Arizona": "AZ","Arkansas": "AR","California": "CA","Colorado": "CO",
               "Connecticut": "CT", "Delaware": "DE","Florida": "FL","Georgia": "GA","Hawaii": "HI","Idaho": "ID",
               "Illinois": "IL","Indiana": "IN","Iowa": "IA", "Kansas": "KS","Kentucky": "KY","Louisiana": "LA",
               "Maine": "ME","Maryland": "MD","Massachusetts": "MA","Michigan": "MI","Minnesota": "MN",
               "Mississippi": "MS","Missouri": "MO","Montana": "MT","Nebraska": "NE","Nevada": "NV",
               "New Hampshire": "NH","New Jersey": "NJ","New Mexico": "NM", "New York": "NY","North Carolina": "NC",
               "North Dakota": "ND","Ohio": "OH","Oklahoma": "OK","Oregon": "OR","Pennsylvania": "PA",
               "Rhode Island": "RI", "South Carolina": "SC","South Dakota": "SD","Tennessee": "TN","Texas": "TX",
               "Utah": "UT","Vermont": "VT","Virginia": "VA","Washington": "WA", "West Virginia": "WV",
               "Wisconsin": "WI","Wyoming": "WY","District of Columbia": "DC","U.S. Total": "US",
               "New England": "New England","Middle Atlantic": "Middle Atlantic",
               "East North Central":"East North Central","West North Central":"West North Central",
               "South Atlantic":"South Atlantic","East South Central":"East South Central",
               "West South Central":"West South Central","Mountain":"Mountain",
               "Pacific Contiguous":"Pacific Contiguous","Pacific Noncontiguous":"Pacific Noncontiguous",
               "US Average":'US', 'US Total':'US'
                }
states_for_prices = []
for key, value in abbrev_dict.items():
    states_for_prices.append(value)
states_for_prices = set(states_for_prices)


# In[69]:


# 1994 through 2001 price data is converted from pdf to csv and must each be formatted separately

# 1994 - Renaming columns
p1994.rename(columns = {p1994.columns[0]:'State', 'Unnamed: 29':'Residential', 'Unnamed: 34':'Commercial', 'Unnamed: 46':'Industrial'}, inplace = True)
# Finding and isolating required data
#p1994[p1994['State'] == '22                                            Energy Information Administration/ Electric Sales and Revenue 1994']
# Isolating required data
for_dropping1 = list(range(0,609,1))
for_dropping2 = list(range(674,13918,1))
p1994.drop(for_dropping1, inplace = True)
p1994.drop(for_dropping2, inplace = True)
p1994.dropna(axis = 'columns', how = 'all', inplace = True)
p1994.drop(columns=['Unnamed: 26', 'Unnamed: 36', 'Unnamed: 53', 'Unnamed: 54', 'Unnamed: 61', 'Unnamed: 62'], inplace = True)
p1994.dropna(inplace = True)
p1994['Year'] = '1994'
p1994.reset_index(drop = True, inplace = True)
# Changing datatypes
p1994['Residential'] = p1994.Residential.apply(float)
p1994['Commercial'] = p1994.Commercial.apply(float)
p1994['Industrial'] = p1994.Industrial.apply(float)
p1994['State'] = p1994.State.str.replace('.', '')
p1994['State'] = p1994.State.apply(str)


# 1995 - Renaming columns
p1995.rename(columns = {p1995.columns[0]:'State', 'Unnamed: 21':'Residential', 'Unnamed: 27':'Commercial', 'Unnamed: 32':'Industrial'}, inplace = True)
# Finding and isolating required data
#p1995[p1995['State'] == 'Table 12.    Average Revenue per Kilowatthour by Sector, Census Division, and State, 1995\n(Cents)']
# Isolating required data
for_dropping1 = list(range(0,632,1))
for_dropping2 = list(range(696,6371,1))
p1995.drop(for_dropping1, inplace = True)
p1995.drop(for_dropping2, inplace = True)
p1995.dropna(axis = 'columns', how = 'all', inplace = True)
p1995.drop(columns=['Unnamed: 19', 'Unnamed: 25', 'Unnamed: 31', 'Unnamed: 36', 'Unnamed: 37', 'Unnamed: 40', 'Unnamed: 42'], inplace = True)
p1995.dropna(inplace = True)
p1995['Year'] = '1995'
p1995.reset_index(drop = True, inplace = True)
# Changing datatypes
p1995['Residential'] = p1995.Residential.apply(float)
p1995['Commercial'] = p1995.Commercial.apply(float)
p1995['Industrial'] = p1995.Industrial.apply(float)
p1995['State'] = p1995.State.str.replace('.', '')
p1995['State'] = p1995.State.apply(str)


# 1996 - Renaming columns
p1996.rename(columns = {p1996.columns[0]:'State', 'Unnamed: 27':'Residential', 'Unnamed: 35':'Commercial', 'Unnamed: 40':'Industrial'}, inplace=True)
# Finding and isolating required data
#p1996[p1996['State'] == 'Table 12.    Average Revenue per Kilowatthour by Sector, Census Division, and State, 1996\n(Cents)']
# Isolating required data
for_dropping1 = list(range(0,631,1))
for_dropping2 = list(range(695,6196,1))
p1996.drop(for_dropping1, inplace = True)
p1996.drop(for_dropping2, inplace = True)
p1996.dropna(axis = 'columns', how = 'all', inplace = True)
p1996.drop(columns=['Unnamed: 25', 'Unnamed: 33', 'Unnamed: 39', 'Unnamed: 45', 'Unnamed: 48', 'Unnamed: 50'], inplace = True)
p1996.dropna(inplace = True)
p1996['Year'] = '1996'
p1996.reset_index(drop = True, inplace = True)
# Changing datatypes
p1996['Residential'] = p1996.Residential.apply(float)
p1996['Commercial'] = p1996.Commercial.apply(float)
p1996['Industrial'] = p1996.Industrial.apply(float)
p1996['State'] = p1996.State.str.replace('.', '')
p1996['State'] = p1996.State.apply(str)


# 1997 - Renaming columns
p1997.rename(columns = {p1997.columns[0]:'State', 'Unnamed: 31':'Residential', 'Unnamed: 39':'Commercial', 'Unnamed: 46':'Industrial'}, inplace=True)
# Finding and isolating required data
#p1997[p1997['State'] == 'Table 12.    Average Revenue per Kilowatthour by Sector, Census Division, and State, 1997\n(Cents)']
# Isolating required data
for_dropping1 = list(range(0,728,1))
for_dropping2 = list(range(792,6290,1))
p1997.drop(for_dropping1, inplace = True)
p1997.drop(for_dropping2, inplace = True)
p1997.dropna(axis = 'columns', how = 'all', inplace = True)
p1997.drop(columns=['Unnamed: 28', 'Unnamed: 36', 'Unnamed: 44', 'Unnamed: 52', 'Unnamed: 53', 'Unnamed: 58', 'Unnamed: 60'], inplace = True)
p1997.dropna(inplace = True)
p1997['Year'] = '1997'
p1997.reset_index(drop = True, inplace = True)
# Changing datatypes
p1997['Residential'] = p1997.Residential.apply(float)
p1997['Commercial'] = p1997.Commercial.apply(float)
p1997['Industrial'] = p1997.Industrial.apply(float)
p1997['State'] = p1997.State.str.replace('.', '')
p1997['State'] = p1997.State.apply(str)


# 1998 - Renaming columns
p1998.rename(columns = {p1998.columns[0]:'State', 'Unnamed: 31':'Residential', 'Unnamed: 38':'Commercial', 'Unnamed: 46':'Industrial'}, inplace=True)
# Finding and isolating required data
#p1998[p1998['State'] == 'Table 12.    Average Revenue per Kilowatthour by Sector, Census Division, and State, 1998\n(Cents)']
# Isolating required data
for_dropping1 = list(range(0,756,1))
for_dropping2 = list(range(820,7192,1))
p1998.drop(for_dropping1, inplace = True)
p1998.drop(for_dropping2, inplace = True)
p1998.dropna(axis = 'columns', how = 'all', inplace = True)
p1998.drop(columns=['Unnamed: 30', 'Unnamed: 45', 'Unnamed: 53', 'Unnamed: 54', 'Unnamed: 61', 'Unnamed: 63'], inplace = True)
p1998.dropna(inplace = True)
p1998['Year'] = '1998'
p1998.reset_index(drop = True, inplace = True)
# Changing datatypes
p1998['Residential'] = p1998.Residential.apply(float)
p1998['Commercial'] = p1998.Commercial.apply(float)
p1998['Industrial'] = p1998.Industrial.apply(float)
p1998['State'] = p1998.State.str.replace('.', '')
p1998['State'] = p1998.State.apply(str)


# 1999 - Renaming columns
p1999.rename(columns = {p1999.columns[0]:'State', 'Unnamed: 26':'Residential', 'Unnamed: 32':'Commercial', 'Unnamed: 38':'Industrial'}, inplace = True)
# Finding and isolating required data
#p1999[p1999['State'] == '(Cents)']
# Isolating required data
for_dropping1 = list(range(0,788,1))
for_dropping2 = list(range(852,7778,1))
p1999.drop(for_dropping1, inplace = True)
p1999.drop(for_dropping2, inplace = True)
p1999.dropna(axis = 'columns', how = 'all', inplace = True)
p1999.drop(columns=['Unnamed: 24', 'Unnamed: 37', 'Unnamed: 43', 'Unnamed: 44', 'Unnamed: 48', 'Unnamed: 49'], inplace = True)
p1999.dropna(inplace = True)
p1999['Year'] = '1999'
p1999.reset_index(drop = True, inplace = True)
# Changing datatypes
p1999['Residential'] = p1999.Residential.apply(float)
p1999['Commercial'] = p1999.Commercial.apply(float)
p1999['Industrial'] = p1999.Industrial.apply(float)
p1999['State'] = p1999.State.str.replace('.', '')
p1999['State'] = p1999.State.apply(str)


# 2000 - Renaming columns
p2000.rename(columns = {p2000.columns[0]:'State', 'Unnamed: 20':'Residential', 'Unnamed: 29':'Commercial','Unnamed: 38':'Industrial'}, inplace = True)
# Finding and isolating required data
#p2000[p2000['State'] == '(Cents)']
# Isolating required data
for_dropping1 = list(range(0,433,1))
for_dropping2 = list(range(497,8361,1))
p2000.drop(for_dropping1, inplace = True)
p2000.drop(for_dropping2, inplace = True)
p2000.dropna(axis = 'columns', how = 'all', inplace = True)
p2000.drop(columns=['Unnamed: 13', 'Unnamed: 25', 'Unnamed: 33', 'Unnamed: 42', 'Unnamed: 51', 'Unnamed: 53'], inplace = True)
p2000.dropna(inplace=True)
p2000['Year'] = '2000'
p2000.reset_index(drop = True, inplace = True)
# Changing datatypes
p2000['Residential'] = p2000.Residential.apply(float)
p2000['Commercial'] = p2000.Commercial.apply(float)
p2000['Industrial'] = p2000.Industrial.apply(float)
p2000['State'] = p2000.State.str.replace('.', '')
p2000['State'] = p2000.State.apply(str)


# 2001 - Renaming columns
p2001.rename(columns = {p2001.columns[0]:'State', 'Unnamed: 3':'Residential', 'Unnamed: 4':'Commercial','Unnamed: 8':'Industrial'}, inplace = True)
# Finding and isolating required data
#p2001[p2001['State'] == 'Table 1d. Average Revenue per Kilowatthour for Bundled and Unbundled Consumers by Sector, Census Division, and State, 2001']
# Isolating required data
for_dropping1 = list(range(0,398,1))
for_dropping2 = list(range(463,13149,1))
p2001.drop(for_dropping1, inplace = True)
p2001.drop(for_dropping2, inplace = True)
p2001.dropna(axis = 'columns', how = 'all', inplace = True)
p2001.drop(columns = ['Unnamed: 11', 'Unnamed: 14'], inplace = True)
p2001.dropna(inplace = True)
p2001['Year'] = '2001'
p2001.reset_index(drop = True, inplace = True)
# Changing datatypes
p2001['Residential'] = p2001.Residential.apply(float)
p2001['Commercial'] = p2001.Commercial.apply(float)
p2001['Industrial'] = p2001.Industrial.apply(float)
p2001['State'] = p2001.State.apply(str)

# Combining all 2001 - 1994 dataframes for ease of joining with all years later
dfs01_94 = [p1994, p1995, p1996, p1997, p1998, p1999, p2000, p2001]
for df in dfs01_94:
    df['State'] = df['State'].str.strip()
    df.replace({"State": abbrev_dict}, inplace = True)

dfs01_94 = pd.concat([p1994, p1995, p1996, p1997, p1998, p1999, p2000, p2001])

# Creating a dictionary of dataframes for 1994 - 2001 price data
dfs01_94_dict = {}
for state in states_for_prices:
    dfs01_94_dict[state] = dfs01_94[dfs01_94['State'] == state]
    dfs01_94_dict[state].set_index('Year', inplace=True)
    dfs01_94_dict[state].columns.name = state
    dfs01_94_dict[state].drop(columns = 'State', inplace = True)
    dfs01_94_dict[state] = pd.concat([dfs01_94_dict[state], headcpi_df.loc[['1994','1995','1996','1997','1998','1999','2000','2001']]], axis=1)
    dfs01_94_dict[state]['Residential_adj'] = round(dfs01_94_dict[state]['Residential'] / (dfs01_94_dict[state]['CPI'] / 100), 2)
    dfs01_94_dict[state]['Commercial_adj'] = round(dfs01_94_dict[state]['Commercial'] / (dfs01_94_dict[state]['CPI'] / 100), 2)
    dfs01_94_dict[state]['Industrial_adj'] = round(dfs01_94_dict[state]['Industrial'] / (dfs01_94_dict[state]['CPI'] / 100), 2)
    dfs01_94_dict[state] = pd.concat([dfs01_94_dict[state], cpi_df.loc[['1994','1995','1996','1997','1998','1999','2000','2001']]], axis = 1)

# Discarding regional data. Add back once regional data is strucutred to accept it
dfs01_94_dict.pop('New England')
dfs01_94_dict.pop('Middle Atlantic')
dfs01_94_dict.pop('East North Central')
dfs01_94_dict.pop('West North Central')
dfs01_94_dict.pop('South Atlantic')
dfs01_94_dict.pop('East South Central')
dfs01_94_dict.pop('West South Central')
dfs01_94_dict.pop('Mountain')
dfs01_94_dict.pop('Pacific Contiguous')
dfs01_94_dict.pop('Pacific Noncontiguous');


# In[70]:


# Test
#dfs01_94_dict['US']


# In[71]:


# 2002 data is imported through 3 csv files, 1 per consumer type

# Renaming and organizing according to consumer type
for df in dfs2002:
    df.rename(columns={df.columns[0]:'State'}, inplace = True)
    df.drop(columns=['Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'], inplace = True)
    df.replace({"State": abbrev_dict}, inplace = True)

    if df is p2002Res:
        df.rename(columns = {'Unnamed: 5': 'Residential'}, inplace = True)
        dfResS = df[df['State'].isin(states_for_prices)]
        dfResS.drop(columns = 'Residential', inplace = True)
        dfResS.reset_index(drop = True, inplace = True)
        dfResP = df[df['State'] == ' State Total']
        dfResP.reset_index(drop = True, inplace = True)
        dfResP.drop(columns = 'State', inplace = True)
        dfs2002[0] = pd.concat([dfResS, dfResP], axis = 1)
    elif df is p2002Com:
        df.rename(columns = {'Unnamed: 5': 'Commercial'}, inplace = True)
        dfComS = df[df['State'].isin(states_for_prices)]
        dfComS.drop(columns = 'Commercial', inplace = True)
        dfComS.reset_index(drop = True, inplace = True)
        dfComP = df[df['State'] == ' State Total']
        dfComP.reset_index(drop = True, inplace = True)
        dfComP.drop(columns = 'State', inplace = True)
        dfs2002[1] = pd.concat([dfComS, dfComP], axis = 1)
    elif df is p2002Ind:
        df.rename(columns = {'Unnamed: 5': 'Industrial'}, inplace = True)
        dfIndS = df[df['State'].isin(states_for_prices)]
        dfIndS.drop(columns = 'Industrial', inplace = True)
        dfIndS.reset_index(drop = True, inplace = True)
        dfIndP = df[df['State'] == ' State Total']
        dfIndP.reset_index(drop = True, inplace = True)
        dfIndP.drop(columns = 'State', inplace = True)
        dfs2002[2] = pd.concat([dfIndS, dfIndP], axis = 1)

# Changing datatypes and adding inflation adjustments
p2002 = dfs2002[0]
p2002['Commercial'] = dfs2002[1]['Commercial']
p2002['Industrial'] = dfs2002[2]['Industrial']
p2002['Year'] = '2002'
p2002['Residential'] = p2002.Residential.apply(float)
p2002['Commercial'] = p2002.Commercial.apply(float)
p2002['Industrial'] = p2002.Industrial.apply(float)
usline = {'State': 'US', 'Residential': 0, 'Commercial': 0, 'Industrial': 0, 'Year': '2002'}
usline = pd.DataFrame(data = usline, index = [51])
usline['Residential'] = round(p2002['Residential'].mean(), 2)
usline['Commercial'] = round(p2002['Commercial'].mean(), 2)
usline['Industrial'] = round(p2002['Industrial'].mean(), 2)
p2002 = pd.concat([p2002, usline])
p2002.set_index('Year', inplace = True)
p2002['CPI'] = headline_cpi[8]
p2002['Residential_adj'] = round(p2002['Residential'] / (p2002['CPI'] / 100), 2)
p2002['Commercial_adj'] = round(p2002['Commercial'] / (p2002['CPI'] / 100), 2)
p2002['Industrial_adj'] = round(p2002['Industrial'] / (p2002['CPI'] / 100), 2)
p2002['Core_CPI'] = core_cpi[8]

# creating dictionary of dataframes. State as key.
p2002_dict = {}
for state in list(p2002['State']):
    p2002_dict[state] = p2002[p2002['State'] == state]
    p2002_dict[state].drop(columns = 'State', inplace = True)


# In[72]:


p2002_dict['US']


# In[73]:


# Organizing 2003 Price Data - Data came in 3 csv files by consumer type and was organized by each generator by state

#def reading_prices_2003(dflist):
for df in dfs2003:
    df.drop(columns={df.columns[0]}, inplace = True)
    df.rename(columns = {'Unnamed: 1':'State'}, inplace = True)
    df.drop(columns=['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4', 'Unnamed: 5'], inplace = True)
    df.dropna(axis = 'columns', how = 'all', inplace = True)
    df.dropna(inplace = True)
    df.reset_index(drop = True, inplace = True)
    df.drop(0 , axis = 0, inplace = True)
    df.reset_index(drop = True, inplace = True)
    if df is p2003Res:
        df.rename(columns = {'Unnamed: 6':'Residential'}, inplace = True)
        df['Residential'] = df.Residential.apply(float)
        dfs2003[0] = pd.DataFrame(round(df.groupby('State')['Residential'].mean(), 2))
        dfs2003[0].reset_index(inplace=True)
    elif df is p2003Ind:
        df.rename(columns = {'Unnamed: 6':'Industrial'}, inplace = True)
        df['Industrial'] = df.Industrial.apply(float)
        dfs2003[1] = pd.DataFrame(round(df.groupby('State')['Industrial'].mean(), 2))
        dfs2003[1].reset_index(inplace=True)
    elif df is p2003Com:
        df.rename(columns = {'Unnamed: 6':'Commercial'}, inplace = True)
        df['Commercial'] = df.Commercial.apply(float)
        dfs2003[2] = pd.DataFrame(round(df.groupby('State')['Commercial'].mean(), 2))
        dfs2003[2].reset_index(inplace=True)

# Changing datatypes and adding inflation adjustments
p2003 = dfs2003[0]
p2003['Commercial'] = dfs2003[2]['Commercial']
p2003['Industrial'] = dfs2003[1]['Industrial']
p2003['Year'] = '2003'
usline = {'State': 'US', 'Residential': 0, 'Commercial': 0, 'Industrial': 0, 'Year': '2003'}
usline = pd.DataFrame(data = usline, index = [0])
usline['Residential'] = round(p2003['Residential'].mean(), 2)
usline['Commercial'] = round(p2003['Commercial'].mean(), 2)
usline['Industrial'] = round(p2003['Industrial'].mean(), 2)
p2003 = pd.concat([p2003, usline])
p2003.set_index('Year', inplace = True)
p2003['CPI'] = headline_cpi[9]
p2003['Residential_adj'] = round(p2003['Residential'] / (p2003['CPI'] / 100), 2)
p2003['Commercial_adj'] = round(p2003['Commercial'] / (p2003['CPI'] / 100), 2)
p2003['Industrial_adj'] = round(p2003['Industrial'] / (p2003['CPI'] / 100), 2)
p2003['Core_CPI'] = core_cpi[9]

# creating dictionary of dataframes. State as key.
p2003_dict = {}
for state in list(p2003['State']):
    p2003_dict[state] = p2003[p2003['State'] == state]
    p2003_dict[state].drop(columns = 'State', inplace = True)


# In[74]:


#Test
#p2003_dict['US']


# In[75]:


# Function for standardizing format of each dataframe.
# Renamed columns, removed null values, removed transportation pricing as their were signicant quantities of null values
# Added a column with year to each dataframe for organization later on
# Concatenated all price dataframes years 2004 - 2022
# Restructured the price data for consistency with generation data, a dictionary with dataframes by state

def reading_prices_1(dfs):
# Renaming and standardizing format
    for df in dfs:
        df.rename(columns={df.columns[0]:'State', 'Unnamed: 1':'Residential','Unnamed: 2':'Commercial',
                           'Unnamed: 3':'Industrial','Unnamed: 4':'Transportation'}, inplace = True)
        df.drop(columns = ['Unnamed: 5', 'Transportation'], inplace = True)
        df.dropna(axis = 'columns', how = 'all', inplace = True)        
        df.dropna(inplace = True)
        df.reset_index(drop = True, inplace = True)
        df.drop(0 , axis = 0, inplace = True)
        df.reset_index(drop = True, inplace = True)       
        df['State'] = df['State'].str.strip()
        df.replace({"State": abbrev_dict}, inplace = True)
# Year will later serve as index    
        if df is p2022:
            df['Year'] = '2022'
        elif df is p2021:
            df['Year'] = '2021'
        elif df is p2020:
            df['Year'] = '2020'
        elif df is p2019:
            df['Year'] = '2019'
        elif df is p2018:
            df['Year'] = '2018'
        elif df is p2017:
            df['Year'] = '2017'
        elif df is p2016:
            df['Year'] = '2016'
        elif df is p2015:
            df['Year'] = '2015'
        elif df is p2014:
            df['Year'] = '2014'
        elif df is p2013:
            df['Year'] = '2013'
        elif df is p2012:
            df['Year'] = '2012'
        elif df is p2011:
            df['Year'] = '2011'
        elif df is p2010:
            df['Year'] = '2010'
        elif df is p2009:
            df['Year'] = '2009'
        elif df is p2008:
            df['Year'] = '2008'
        elif df is p2007:
            df['Year'] = '2007'
        elif df is p2006:
            df['Year'] = '2006'
        elif df is p2005:
            df['Year'] = '2005'
        elif df is p2004:
            df['Year'] = '2004'
# Creating dictionary of datafranes with state as key to be concatenated            
    prices = pd.concat(dfs)
    for state in set(prices['State']):
        state_prices[state] = prices[prices['State'] == state]
        state_prices[state].set_index('Year', inplace = True)
        state_prices[state].columns.name = state
        state_prices[state].drop(columns = 'State', inplace = True)
        state_prices[state]['Residential'] = state_prices[state].Residential.apply(float)
        state_prices[state]['Commercial'] = state_prices[state].Commercial.apply(float)
        state_prices[state]['Industrial'] = state_prices[state].Industrial.apply(float)
        state_prices[state] = state_prices[state][::-1]
        state_prices[state]['CPI'] = headline_cpi[10::]
        state_prices[state]['Residential_adj'] = round(state_prices[state]['Residential'] / (state_prices[state]['CPI'] / 100), 2)
        state_prices[state]['Commercial_adj'] = round(state_prices[state]['Commercial'] / (state_prices[state]['CPI'] / 100), 2)
        state_prices[state]['Industrial_adj'] = round(state_prices[state]['Industrial'] / (state_prices[state]['CPI'] / 100), 2)
        state_prices[state]['Core_CPI'] = core_cpi[10::]
        
# Dropping regional data to add back once generation data can be formatted to accept
    state_prices.pop('New England')
    state_prices.pop('Middle Atlantic')
    state_prices.pop('East North Central')
    state_prices.pop('West North Central')
    state_prices.pop('South Atlantic')
    state_prices.pop('East South Central')
    state_prices.pop('West South Central')
    state_prices.pop('Mountain')
    state_prices.pop('Pacific Contiguous')
    state_prices.pop('Pacific Noncontiguous')
# Concatenating all dictionaries of dataframes    
    for state in state_prices:
        state_pricing[state] = pd.concat([dfs01_94_dict[state], p2002_dict[state], p2003_dict[state], state_prices[state]])
           


# In[76]:


reading_prices_1(dfs)


# In[78]:


# Test
#state_pricing['US']

