import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
import os

def perform_time_series_analysis(df):
    statistics = []
    
    for column in df.columns:
       
        column_data = df[column].dropna()
        
        # Perform time series analysis
        decomposition = sm.tsa.seasonal_decompose(column_data, model='additive')
        
        # Calculate numerical statistics
        mean = column_data.mean()
        std = column_data.std()
        autocorr = column_data.autocorr()
        
      
        stats = {'Commodity': column,
                 'Mean': mean,
                 'Standard Deviation': std,
                 'Autocorrelation': autocorr}
        
        # Append the dictionary to the list
        statistics.append(stats)
        

        plt.figure(figsize=(12, 8))
        plt.subplot(411)
        plt.plot(column_data.index, column_data, label='Original')
        plt.legend(loc='best')
        plt.subplot(412)
        plt.plot(column_data.index, decomposition.trend, label='Trend')
        plt.legend(loc='best')
        plt.subplot(413)
        plt.plot(column_data.index, decomposition.seasonal, label='Seasonal')
        plt.legend(loc='best')
        plt.subplot(414)
        plt.plot(column_data.index, decomposition.resid, label='Residual')
        plt.legend(loc='best')
        plt.tight_layout()
        plt.title(f'{column} - Time Series Analysis')
        plt.show()

    
        plt.close()
    

    statistics_df = pd.DataFrame(statistics)
    

    print(statistics_df)
