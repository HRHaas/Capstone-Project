#!/usr/bin/env python
# coding: utf-8

# In[1]:


from Step1_Processing_Energy_Generation_Data import *
from Step2_Processing_Price_Data import *
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import linear_model
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import statsmodels
from sklearn import metrics
from IPython.display import display


# In[18]:


def Energy_Price_Impact_Tool():

    combined = {}
    for state in state_list:
        combined[state] = pd.concat([state_mix[state], state_pricing[state], state_gen[state]], axis = 1)
        #combined[state].drop(['2003','2002','2001','2000','1999','1998','1997','1996','1995','1994','1993','1992','1991','1990'], inplace = True)
        combined[state].dropna(inplace = True)
        combined[state].columns.name = state
    
    
    state = str(input("Enter your abbreviated state name or US for national data: "))
    state = state.upper()
    
    consumer_type = str(input("Enter your consumer type, type R for Residential, C for Commercial, I for Industrial: "))
    consumer_type = consumer_type.upper()
    
    if consumer_type == 'R':
        consumer_type = 'Residential'
        consumer_type_real = 'Residential_adj'
    elif consumer_type == 'C':
        consumer_type = 'Commercial'
        consumer_type_real = 'Commercial_adj'        
    elif consumer_type == 'I':
        consumer_type = 'Industrial'
        consumer_type_real = 'Industrial_adj'
    elif consumer_type != 'R' or consumer_type != 'C' or consumer_type != 'I':
        return print('Error: Consumer type entered incorrectly, please restart')
        
    
    independent_vars_selection = str(input("Enter your predictive factor type, P for Percentage of Energy Source mix, or G for Generation in MWh: "))
    independent_vars_selection = independent_vars_selection.upper()
    
    if independent_vars_selection == 'P':
        visual = combined[state][[consumer_type,'Core_CPI', consumer_type_real, 'Renewables_pct','Fossil_Fuels_pct','Nuclear_pct', 'Pumped_Storage_pct', 'Other_pct']]
        display(visual)
        independent_vars = ['Renewables_pct', 'Fossil_Fuels_pct', 'Nuclear_pct', 'Core_CPI']
        # Create the bar plots
        plt.figure(figsize=(10,5)) 
        plt.plot(combined[state][independent_vars[0]],  label=independent_vars[0], linewidth = '4')
        plt.plot(combined[state][independent_vars[1]],  label=independent_vars[1], linewidth = '4')
        plt.plot(combined[state][independent_vars[2]], label=independent_vars[2], linewidth = '4')
        ax = plt.gca()   
        # Add x-axis and y-axis labels and a title
        plt.xlabel('Year')
        plt.ylabel('Percent of all Energy Generation')
        plt.title('Energy Source Share Change Since 1994')
        n = 2  # Keeps every nth label
        [l.set_visible(False) for (i,l) in enumerate(ax.xaxis.get_ticklabels()) if i % n != 0]
        # Add legend
        plt.legend()
        # Show the chart
        plt.show()
    
    elif independent_vars_selection == 'G':
        visual = combined[state][[consumer_type, 'Core_CPI', consumer_type_real, 'Coal', 'Geothermal', 'Hydroelectric Conventional', 'Natural Gas','Nuclear', 'Other', 'Other Biomass', 'Other Gases', 'Petroleum','Pumped Storage', 'Solar Thermal and Photovoltaic', 'Wind','Wood and Wood Derived Fuels', 'Total']]
        display(visual)
        independent_vars = ['Coal','Hydroelectric Conventional','Natural Gas','Nuclear','Petroleum','Solar Thermal and Photovoltaic','Wind','Core_CPI']
        # Create the bar plots
        plt.figure(figsize=(10,5)) 
        plt.plot(combined[state][independent_vars[0]],  label=independent_vars[0], linewidth = '4')
        plt.plot(combined[state][independent_vars[1]],  label=independent_vars[1], linewidth = '4')
        plt.plot(combined[state][independent_vars[2]], label=independent_vars[2], linewidth = '4')
        plt.plot(combined[state][independent_vars[3]], label=independent_vars[3], linewidth = '4')
        plt.plot(combined[state][independent_vars[4]], label=independent_vars[4], linewidth = '4')
        plt.plot(combined[state][independent_vars[5]], label=independent_vars[5], linewidth = '4')
        plt.plot(combined[state][independent_vars[6]], label=independent_vars[6], linewidth = '4')
        ax = plt.gca()   
        # Add x-axis and y-axis labels and a title
        plt.xlabel('Year')
        plt.ylabel('Generation in MWh')
        plt.title('Energy Source Generation Change Since 1994')
        n = 2  # Keeps every nth label
        [l.set_visible(False) for (i,l) in enumerate(ax.xaxis.get_ticklabels()) if i % n != 0]
        # Add legend
        plt.legend()
        # Show the chart
        plt.show()
        
    elif independent_vars_selection != 'P' or independent_vars_selection != 'G':
        return print('Error: Predictive factor type entered incorrectly, please restart')
    
    def montecarlo(df):
        global X
        global Y
        X = combined[state][independent_vars]#.values
        y = combined[state][consumer_type]#.values
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = .3)
        global mlr 
        mlr = LinearRegression()  
        mlr.fit(X_train, y_train)
        global y_pred_mlr
        y_pred_mlr= mlr.predict(X_test)
        rsquare = round(mlr.score(X,y)*100, 4)
        meanAbErr = metrics.mean_absolute_error(y_test, y_pred_mlr)
        meanSqErr = metrics.mean_squared_error(y_test, y_pred_mlr)
        rootMeanSqErr = np.sqrt(metrics.mean_squared_error(y_test, y_pred_mlr))
        return round(mlr.score(X,y)*100, 4), meanAbErr, meanSqErr, rootMeanSqErr  #, mlr.intercept_, mlr.coef_

    montecarlo(combined[state])
    outputs = []
    for x in range(1,1001):
        outputs.append(montecarlo(combined[state]));  
    for x in outputs:
        rsquare = x[0].mean()
        meanAbErr = x[1].mean()
        meanSqErr = x[2].mean()
        rootMeanSqErr = x[3].mean()
        
    print(f"\nThe summary statistics for the regression on {independent_vars} for {consumer_type} consumers are:\n")
    print("Intercept: ", mlr.intercept_)
    print("Coefficients:", *list(zip(X, mlr.coef_)))         
    print(f"\nThe R² = {round(rsquare, 4)}")
    print(f"The Mean Absolute Squared Error = {round(meanAbErr,4)}")
    print(f"The Mean Squared Error = {round(meanSqErr,4)}")
    print(f"Root Mean Square Error: {round(rootMeanSqErr, 4)}\n")
    
    
    
    Choice_Price = str(input("Do you want to forecast price? (Y/N): "))
    Choice_Price = Choice_Price.upper()

    if Choice_Price == 'Y':
        if independent_vars_selection == 'P':
            renewable = float(input('\nEnter renewables as a percent of total energy generation: ' ))
            fossilfuel = float(input('Enter fossil fuels as a percent of total energy generation: : ' ))
            nuclear = float(input('Enter nuclear as a percent of total energy generation: '))
            year_input = int(input('Enter the year of your forecast: '))
            forecast_time = year_input - int(combined['US'].index[-1])
            inflation_input = float(input('Enter your assumed inflation rate: '))
            inflation_assumption = []
            for x in range(forecast_time):
                inflation_assumption.append(inflation_input)
            Core_CPI_forecast = [combined[state]['Core_CPI'][-1]]
            for x in inflation_assumption:
                Core_CPI_forecast.append(round((x/100+1) * Core_CPI_forecast[-1], 4))         
            price_prediction = mlr.predict([[renewable, fossilfuel, nuclear, Core_CPI_forecast[-1]]])
        elif independent_vars_selection == 'G':
            #['Coal','Hydroelectric Conventional','Natural Gas','Nuclear','Petroleum','Solar Thermal and Photovoltaic','Wind']
            coal = float(input('\nEnter coal generation in MWh: ' ))
            hydro = float(input('Enter hydro generation in MWh: ' ))
            natgas = float(input('Enter natural gas generation in MWh: '))
            nuclear_gen = float(input('Enter nuclear generation in MWh: '))
            petroleum = float(input('Enter petroleum generation in MWh: '))
            solar = float(input('Enter solar generation in MWh: '))
            wind = float(input('Enter wind generation in MWh: '))
            year_input = int(input('Enter the year of your forecast: '))
            forecast_time = year_input - int(combined['US'].index[-1])
            inflation_input = float(input('Enter your assumed inflation rate: '))
            inflation_assumption = []
            for x in range(forecast_time):
                inflation_assumption.append(inflation_input)
            Core_CPI_forecast = [combined[state]['Core_CPI'][-1]]
            for x in inflation_assumption:
                Core_CPI_forecast.append(round((x/100+1) * Core_CPI_forecast[-1], 4))
            price_prediction = mlr.predict([[coal, hydro, natgas, nuclear_gen, petroleum, solar, wind, Core_CPI_forecast[-1]]])
    elif Choice_Price == 'N':
        return print("\nAnalysis Complete")
    elif Choice_Price != 'Y' or Choice_Price != 'N':
        return print("\nError: price forecast entered incorrectly, please restart to forecast price. Analysis complete.")
        
    # Would like to plot a MLR graph to visualize relationships
    if Choice_Price.upper() == 'Y':
        if consumer_type == 'Residential':
            print("\nYour estimated nominal price in cents per KWh is:", round(*price_prediction,2), ", and the real price is:",round(*(price_prediction / (Core_CPI_forecast[-1]/100)),2))
            print("Your estimated spend per day in USD is: $",round(*(29*price_prediction / 100),2))
            print("Your estimated spend per month in USD is: $",round(*(890*price_prediction / 100),2))
            print("Your estimated spend per year in USD is: $",round(*(10577*price_prediction / 100),2))
            return print('\nAnalysis complete, run cell to restart')
        elif consumer_type == 'Commercial':
            print("\nYour estimated nominal price in cents per KWh is:", round(*(price_prediction),2), "real price is:",round(*(price_prediction / (Core_CPI_forecast[-1]/100)),2))
            return print('\nAnalysis complete, run cell to restart')
        elif consumer_type == 'Industrial':
            print("\nYour estimated nominal price in cents per KWh is:", round(*(price_prediction),2), "real price is:",round(*(price_prediction / (Core_CPI_forecast[-1]/100)),2))
            return print('\nAnalysis complete, run cell to restart')
    else:
        return print('Forecast Complete, please run cell to restart')
    #elif price_forecast == 'N':
    #    return print(f"Analysis Complete")
    


# In[19]:


Energy_Price_Impact_Tool()


# In[4]:


# Graphs to implement

# Create the bar plots
#plt.figure(figsize=(10,5)) 
#plt.plot(combined['US']['Coal'],  label='Renewables', linewidth = '4')
#plt.plot(combined['US']['Wind'],  label='Fossil Fuels', linewidth = '4')
#plt.plot(combined['US']['Nuclear'], label='Nuclear', linewidth = '4')
#ax = plt.gca()   
# Add x-axis and y-axis labels and a title
#plt.xlabel('Year')
#plt.ylabel('Percent of all Energy Generation')
#plt.title('Energy Share Change')
#n = 3  # Keeps every nth label
#[l.set_visible(False) for (i,l) in enumerate(ax.xaxis.get_ticklabels()) if i % n != 0]
# Add legend
#plt.legend()
#change chart size
# Show the chart
#plt.show()


# In[5]:


#def montecarlo(df):
#    X = df[['Renewables_pct', 'Fossil_Fuels_pct', 'Nuclear_pct', 'CPI']]#.values
#    y = df['Residential']#.values
#    
#    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = .3)

#    global mlr
#    mlr = LinearRegression()  
#    mlr.fit(X_train, y_train)
#    global y_pred_mlr
#    y_pred_mlr = mlr.predict(X_test)
    
#    meanAbErr = metrics.mean_absolute_error(y_test, y_pred_mlr)
#    meanSqErr = metrics.mean_squared_error(y_test, y_pred_mlr)
#    rootMeanSqErr = np.sqrt(metrics.mean_squared_error(y_test, y_pred_mlr))

#    return round(mlr.score(X,y)*100, 4), meanAbErr, meanSqErr, rootMeanSqErr

#montecarlo(combined['US'])

#outputs = []
#for x in range(1,101):
#    outputs.append(montecarlo(combined['US']));  

#for x in outputs:
#    rsquare = x[0].mean()
#    MAE = x[1].mean()
#    MSE = x[2].mean()
#    RMSE = x[3].mean()

#print("Intercept: ", mlr.intercept_)
#print("Coefficients:", *list(zip(X, mlr.coef_)))    
#print(f"\nThe R² = {round(rsquare, 4)}")
#print(f"The Mean Absolute Squared Error = {round(MAE,4)}")
#print(f"The MSE = {round(MSE,4)}")

#price_prediction = mlr.predict([[21.29,60.35,18.24,158.9534]])
#print("The forecasted price is", round(*price_prediction, 2))


# In[6]:


# Use a for loop to run 100 times and find avg? or just use random state

#X = combined['US'][['Coal','Hydroelectric Conventional','Natural Gas','Nuclear','Petroleum','Solar Thermal and Photovoltaic','Total','Wind']]#.values
#y = combined['US']['Residential']#.values

#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = .3, random_state = 4)

#mlr = LinearRegression()  
#mlr.fit(X_train, y_train)

#print("Intercept: ", mlr.intercept_)
#print("Coefficients:")
#print(list(zip(X, mlr.coef_)))


#y_pred_mlr= mlr.predict(X_test)
#mlr_diff = pd.DataFrame({'Actual value': y_test, 'Predicted value': y_pred_mlr})
#mlr_diff.head()

#meanAbErr = metrics.mean_absolute_error(y_test, y_pred_mlr)
#meanSqErr = metrics.mean_squared_error(y_test, y_pred_mlr)
#rootMeanSqErr = np.sqrt(metrics.mean_squared_error(y_test, y_pred_mlr))
#print('\nR squared: {:.2f}'.format(mlr.score(X,y)*100))
#print('Mean Absolute Error:', meanAbErr)
#print('Mean Square Error:', meanSqErr)
#print('Root Mean Square Error:', rootMeanSqErr)

#price_prediction = mlr.predict([[21, 60, 18, cpi_forecast[-1]]])
#price_prediction


# In[7]:


#Working choice option for X's



#def test():
#    independent_vars_selection = str(input("Enter your predictive factor type, P for Percentage of Energy Source, G for Generation in MWh: "))
#    Choice0 = str(input("Would you like to choose your independent variables? (Y/N)"))
#    
#    if independent_vars_selection.upper() == 'P':
#        if Choice0.upper() == 'Y':
#            independent_vars = []
#            ChoiceP1 = input('Would you like to include Renewable Energy? (Y/N):')
#            if ChoiceP1.upper() == 'Y':
#                ChoiceP1 = 'Renewable_pct'
#            #elif ChoiceP1 == 'N':
#            #    ChoiceP1 = 'N'
#            ChoiceP2 = input('Would you like to include Fossil Fuels? (Y/N):')
#            if ChoiceP2.upper() == 'Y':
#                ChoiceP2 = 'Fossil_Fuels_pct'
#            ChoiceP3 = input('Would you like to include Nuclear Energy? (Y/N):')
#            if ChoiceP3.upper() == 'Y':
#                ChoiceP3 = 'Nuclear_pct'
#            ChoiceP4 = input('Would you like to include Pumped Storage Energy? (Y/N):')
#            if ChoiceP4.upper() == 'Y':
#                ChoiceP4 = 'Pumped_Storage_pct'
#            ChoiceP5 = input('Would you like to include the Other Energy Category? (Y/N):')
#            if ChoiceP5.upper() == 'Y':
#                ChoiceP5 = 'Other_pct'
#            pricechoices = [ChoiceP1, ChoiceP2, ChoiceP3, ChoiceP4, ChoiceP5]
#            for x in pricechoices:
#                if x != 'N':
#                    independent_vars.append(x)
#            print(independent_vars)
#        elif Choice0.upper() =='N':
#            independent_vars = ['Renewables_pct', 'Fossil_Fuels_pct', 'Nuclear_pct']


# In[8]:


#test()

