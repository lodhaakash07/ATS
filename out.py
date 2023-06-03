main.py
import pandas as pd
import matplotlib.pyplot as plt
from utils.data_loader import load_commodities_data
import numpy as np
from portfolio.portfolio import Portfolio
from backtesting.backtester import Backtester
from strategies.ta_strategy import TA_Strategies
import statsmodels.api as sm
import warnings
warnings.filterwarnings("ignore")

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

    df['Commodity Market Factor'] = market_factor

    # Plot the commodity market factor
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df['Commodity Market Factor'])
    plt.xlabel('Date')
    plt.ylabel('Commodity Market Factor')
    plt.title('Commodity Market Factor - Weighted Average')
    plt.grid(True)
    plt.show()

    # Print descriptive statistics for the commodity market factor
    market_factor_statistics = df['Commodity Market Factor'].describe()
    print('\nCommodity Market Factor - Descriptive Statistics:')
    print(market_factor_statistics)


# Load the data from the Excel file
file_path = 'data/raw/Commodities Data thru 18May23.xlsx'
df = load_commodities_data(file_path)


# Set the date column as the index
df.set_index('Dates', inplace=True)

# Perform time series analysis
#perform_time_series_analysis(df)

# Calculate commodity market factor
#calculate_commodity_market_factor(df)

strategy = TA_Strategies(rsi_window=9, ma_short_period=3, ma_long_period=21, bb_window=20)

portfolio = Portfolio(initial_capital=1)

risk_percentage = 5

# Create an instance of the Backtester class
backtester = Backtester(df.copy(), strategy, risk_percentage, portfolio)

backtester.execute_trades()
main.py
import pandas as pd
import matplotlib.pyplot as plt
from utils.data_loader import load_commodities_data
import numpy as np
from portfolio.portfolio import Portfolio
from backtesting.backtester import Backtester
from strategies.ta_strategy import TA_Strategies
import statsmodels.api as sm
import warnings
warnings.filterwarnings("ignore")

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

    df['Commodity Market Factor'] = market_factor

    # Plot the commodity market factor
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df['Commodity Market Factor'])
    plt.xlabel('Date')
    plt.ylabel('Commodity Market Factor')
    plt.title('Commodity Market Factor - Weighted Average')
    plt.grid(True)
    plt.show()

    # Print descriptive statistics for the commodity market factor
    market_factor_statistics = df['Commodity Market Factor'].describe()
    print('\nCommodity Market Factor - Descriptive Statistics:')
    print(market_factor_statistics)


# Load the data from the Excel file
file_path = 'data/raw/Commodities Data thru 18May23.xlsx'
df = load_commodities_data(file_path)
df= df[:1000]

# Set the date column as the index
df.set_index('Dates', inplace=True)

# Perform time series analysis
#perform_time_series_analysis(df)

# Calculate commodity market factor
#calculate_commodity_market_factor(df)

strategy = TA_Strategies(rsi_window=9, ma_short_period=3, ma_long_period=21, bb_window=20)

portfolio = Portfolio(initial_capital=1)

risk_percentage = 5

# Create an instance of the Backtester class
backtester = Backtester(df.copy(), strategy, risk_percentage, portfolio)

backtester.execute_trades()
