#!/usr/bin/env python
# coding: utf-8

# In[82]:


import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None  # default='warn'


# # Step 1) Processing Energy Generation Data

# In[83]:


# Importing annual generation data from csv file

annual_netgen = pd.read_csv('./Data-CSV/annual_generation_state.csv')


# In[84]:


# Cleaning Dataframe

# Renaming columns
annual_netgen.rename(columns = {annual_netgen.columns[0]:'Year', 'Unnamed: 1':'State','Unnamed: 2':'Producer_Type','Unnamed: 3':'Energy_Source','Unnamed: 4':'Generation_MWh'}, inplace = True)

# Dropping extra columns (null values)
annual_netgen.dropna(axis='columns', inplace = True)

# Dropping First row
annual_netgen = annual_netgen.drop( 0 , axis = 0)

# Removing commas from Generation column to transform type to int
annual_netgen = annual_netgen.apply(lambda x: x.str.replace(',', ''))

# Transforming Generation column to int from str
annual_netgen['Generation_MWh'] = annual_netgen.Generation_MWh.apply(int)

# Standardizing format for 'US Total' Value
annual_netgen = annual_netgen.replace('US-TOTAL','US-Total')
annual_netgen = annual_netgen.replace('US-Total','US')

# Only leave values representative of entire electric power industry
annual_netgen = annual_netgen[annual_netgen['Producer_Type'] == 'Total Electric Power Industry']

# Setting up an empty dictionary to serve as a list of dataframes for each state
state_gen = {}
state_gen_mix = {}
state_class_gen = {}
state_mix = {}

# Setting up lists of unique state and energy source values to sipmlify loops
state_list = list(annual_netgen['State'].unique())
state_list.remove('  ')
energysource_list = list(annual_netgen['Energy_Source'].unique())

New_England = ['CT','ME','MA','NH','RI','VT']
Middle_Atlantic = ['NJ','NY','PA']
East_North_Central = ['IL','IN','MI','OH','WI']
West_North_Central = ['IA','KS','MN','MO','NE','ND','SD']
South_Atlantic = ['DE','DC','FL','GA','MD','NC','SC','VA','WV']
East_South_Central = ['AL','KY','MS','TN']
West_South_Central = ['LA','AR','OK','TX']
Mountain = ['AZ','CO','ID','MT','NV','NM','UT','WY']
Pacific_Contiguous = ['OW','CA','WA']
Pacific_Noncontiguous = ['AK','HI']


# In[85]:


## Add in regions for consistency with Price data
#for state in state_list:
#    if state in New_England:
#        ne = annual_netgen[annual_netgen['State'] == state]
#        annual_netgen = pd.concat([ne, annual_netgen])


# In[86]:


# This loop creates a dictionary of dataframes (State_Gen) for each state (+ DC & US-Total) with the year as the index
# It uses a pivot function to organize generation in MWh by Energy Source for each state
# If a state does not utilize a specific energy source it adds that column in with 0 MWh for standardization purposes

for state in state_list:
    state_gen[state] = annual_netgen.loc[annual_netgen['State'] == state]
    state_gen[state].drop(columns=['State','Producer_Type'], inplace = True)
    state_gen[state] = state_gen[state].pivot(index='Year', columns='Energy_Source')
    state_gen[state].fillna(0, inplace = True)
    state_gen[state] = state_gen[state]['Generation_MWh']
    for source in energysource_list:
        if source not in state_gen[state].columns:
            state_gen[state][source] = 0.0
    state_gen[state].columns.name = state


# In[87]:


# Organizes the energy by source into percentage from generation in MWh

for state in state_list:
    state_gen_mix[state] = state_gen[state].copy()
    for source in energysource_list:
        state_gen_mix[state][source] = round((state_gen[state][source] / state_gen[state]['Total']) * 100,2)


# In[88]:


# This loop takes a copy of each dataframe from State_Gen and organizes it by the EIA's energy classifications
# Dictionary of dataframes is called State_Class_Gen as it has generation in MWh by energy classification

for state in state_list:
    state_class_gen[state] = state_gen[state].copy()
    state_class_gen[state]['Nuclear_Gen'] = state_class_gen[state]['Nuclear']
    state_class_gen[state]['Renewables_Gen'] = state_class_gen[state]['Wind'] + state_class_gen[state]['Wood and Wood Derived Fuels'] + state_class_gen[state]['Solar Thermal and Photovoltaic'] + state_class_gen[state]['Geothermal'] + state_class_gen[state]['Hydroelectric Conventional'] + state_class_gen[state]['Other Biomass']
    state_class_gen[state]['Fossil_Fuels_Gen'] = state_class_gen[state]['Coal'] + state_class_gen[state]['Other Gases'] + state_class_gen[state]['Petroleum'] + state_class_gen[state]['Natural Gas']
    state_class_gen[state]['Pumped_Storage_Gen'] = state_class_gen[state]['Pumped Storage']
    state_class_gen[state]['Others_Gen'] = state_class_gen[state]['Other']
    state_class_gen[state].drop(columns = ['Wind', 'Wood and Wood Derived Fuels', 'Solar Thermal and Photovoltaic', 
                                           'Hydroelectric Conventional', 'Other Biomass', 'Geothermal', 'Coal', 
                                           'Natural Gas', 'Other Gases', 'Petroleum', 'Nuclear', 'Pumped Storage',
                                           'Other'], inplace = True)


# In[89]:


# This loop takes the prior dictionary of dataframes (State_Class_Gen) and finds the percantage of each class
# Dictionary of dataframes is called State_Mix as it has each state's share of all energy classes
# Sum Column can be removed or commented out, is there for validation

for state in state_list:
    state_mix[state] = state_class_gen[state].copy()
    state_mix[state]['Renewables_pct'] = round((state_class_gen[state]['Renewables_Gen'] / state_class_gen[state]['Total']) * 100, 2)
    state_mix[state]['Fossil_Fuels_pct'] = round((state_class_gen[state]['Fossil_Fuels_Gen'] / state_class_gen[state]['Total']) * 100, 2)
    state_mix[state]['Nuclear_pct'] = round((state_class_gen[state]['Nuclear_Gen'] / state_class_gen[state]['Total']) * 100, 2)
    state_mix[state]['Pumped_Storage_pct'] = round((state_class_gen[state]['Pumped_Storage_Gen'] / state_class_gen[state]['Total']) * 100, 2)
    state_mix[state]['Other_pct'] = round((state_class_gen[state]['Others_Gen'] / state_class_gen[state]['Total']) * 100, 2)
    state_mix[state].drop(columns = ['Nuclear_Gen', 'Renewables_Gen', 'Fossil_Fuels_Gen', 'Pumped_Storage_Gen', 'Others_Gen', 'Total'], inplace = True)
    
    #state_mix[state]['SumCheck'] = round(state_mix[state]['Renewables_pct'] + state_mix[state]['Fossil_Fuels_pct'] + state_mix[state]['Nuclear_pct'] + state_mix[state]['Pumped_Storage_pct'] + state_mix[state]['Other_pct'], 2)


# In[90]:


#Test
#state_gen['LA']


# In[91]:


#Test
#state_gen_mix['WA']


# In[92]:


#Test
#state_class_gen['ND']


# In[93]:


#Test
#state_mix['US']

