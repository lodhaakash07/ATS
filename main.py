import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
import os

from utils.data_loader import load_commodities_data
from portfolio.portfolio import Portfolio
from backtesting.backtester import Backtester
from strategies.ta_strategy import TA_Strategies
from backtesting.trade_analytics import generate_trade_analytics
from backtesting.metrics import calculate_metrics

import warnings
warnings.filterwarnings("ignore")

# Create the output folder if it doesn't exist
output_folder = 'output'
os.makedirs(output_folder, exist_ok=True)

def perform_time_series_analysis(df):
    statistics = []
    
    for column in df.columns:
        # Remove missing values
        column_data = df[column].dropna()
        
        # Perform time series analysis
        decomposition = sm.tsa.seasonal_decompose(column_data, model='additive')
        
        # Calculate numerical statistics
        mean = column_data.mean()
        std = column_data.std()
        autocorr = column_data.autocorr()
        
        # Store statistics in a dictionary
        stats = {'Commodity': column,
                 'Mean': mean,
                 'Standard Deviation': std,
                 'Autocorrelation': autocorr}
        
        # Append the dictionary to the list
        statistics.append(stats)
        
        # Plot the original series, trend, seasonal, and residual components
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

        # Save the figure as a PNG image
        plt.savefig(f'{output_folder}/{column}_time_series_analysis.png')
        
        # Close the figure to release memory
        plt.close()
    
    # Create a dataframe from the list of dictionaries
    statistics_df = pd.DataFrame(statistics)
    
    # Print the statistics dataframe
    print(statistics_df)

def calculate_commodity_market_factor(df):
    market_factor = []
    for index, row in df.iterrows():
        available_assets = row.count() - 1  # Exclude the 'Dates' column
        total_return = row.dropna().sum()
        weighted_average = total_return / available_assets
        market_factor.append(weighted_average)

    cmf = pd.DataFrame(market_factor)
    cmf.index = df.index
   
    return cmf
    # Plot the commodity market factor
    plt.figure(figsize=(10, 6))
    plt.plot(cmf.index, cmf)
    plt.xlabel('Date')
    plt.ylabel('Commodity Market Factor')
    plt.title('Commodity Market Factor - Weighted Average')
    plt.grid(True)
    plt.show()

    # Print descriptive statistics for the commodity market factor
    market_factor_statistics = cmf.describe()
    print('\nCommodity Market Factor - Descriptive Statistics:')
    print(market_factor_statistics)

    # Save the figure as a PNG image
    plt.savefig(f'{output_folder}/commodity_market_factor.png')
    
    # Close the figure to release memory
    plt.close()

    return cmf


# Load the data from the Excel file
file_path = 'data/raw/Commodities Data thru 18May23.xlsx'
df = load_commodities_data(file_path)


# Set the date column as the index
df.set_index('Dates', inplace=True)


# Perform time series analysis
print("Summary statistics for each assets")
perform_time_series_analysis(df)

# Calculate commodity market factor
print("Commodity market factor")
cmf=calculate_commodity_market_factor(df)


strategy = TA_Strategies(rsi_window=9, ma_short_period=3, ma_long_period=21, bb_window=20)

portfolio = Portfolio(initial_capital=1)

portfolio_cmf = Portfolio(initial_capital=1)

risk_percentage = 5

# Create an instance of the Backtester class
backtester = Backtester(df.copy(), strategy, risk_percentage, portfolio)
backtester_cmf = Backtester(cmf.copy(), strategy, risk_percentage, portfolio_cmf)

backtester.execute_trades()
backtester_cmf.execute_trades()

# Trade analytics 
print(' Trade analytics for the portfolio')
generate_trade_analytics(portfolio.trade_logs)

print(' Trade Analytics for the Commodity Market Factor')
generate_trade_analytics(portfolio_cmf.trade_logs)


matrics = calculate_metrics(portfolio.trade_logs['pnl'], portfolio_cmf.trade_logs['pnl'])

# Print the metrics
print('Comparing metics of the commodity return vs commodity factor returns')
for key, value in matrics.items():
    print(key + ':', value)
    


