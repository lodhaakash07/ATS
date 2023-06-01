import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from utils.data_loader import load_commodities_data

def perform_time_series_analysis(df):
    for column in df.columns:
        decomposition = sm.tsa.seasonal_decompose(df[column], model='additive')
        
        # Numerical analysis
        mean = df[column].mean()
        std = df[column].std()
        autocorr = df[column].autocorr()
        
        # Print numerical statistics
        print(f'Commodity: {column}')
        print(f'Mean: {mean:.2f}')
        print(f'Standard Deviation: {std:.2f}')
        print(f'Autocorrelation: {autocorr:.2f}')
        print('\n')
        
        # Plot the original, trend, seasonal, and residual components
        plt.figure(figsize=(12, 8))
        plt.subplot(411)
        plt.plot(df.index, df[column], label='Original')
        plt.legend(loc='best')
        plt.subplot(412)
        plt.plot(df.index, decomposition.trend, label='Trend')
        plt.legend(loc='best')
        plt.subplot(413)
        plt.plot(df.index, decomposition.seasonal, label='Seasonality')
        plt.legend(loc='best')
        plt.subplot(414)
        plt.plot(df.index, decomposition.resid, label='Residuals')
        plt.legend(loc='best')
        plt.tight_layout()
        plt.title(f'{column} - Time Series Decomposition')
        plt.show()

def calculate_commodity_market_factor(df):
    weights = pd.Series(1 / len(df.columns), index=df.columns)
    df['Commodity Market Factor'] = df[df.columns].dot(weights)
    
    # Plot the commodity market factor
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df['Commodity Market Factor'])
    plt.xlabel('Date')
    plt.ylabel('Commodity Market Factor')
    plt.title('Commodity Market Factor - Equally Weighted Average')
    plt.grid(True)
    plt.show()
    
    # Print descriptive statistics for the commodity market factor
    market_factor_statistics = df['Commodity Market Factor'].describe()
    print('\nCommodity Market Factor - Descriptive Statistics:')
    print(market_factor_statistics)

# Load the data from the Excel file
file_path = 'data/raw/Commodities Data thru 18May23.xlsx'
df = load_commodities_data(file_path)

# Drop any rows with missing values
df.dropna(inplace=True)

# Set the date column as the index
df.set_index('Dates', inplace=True)

# Perform time series analysis
perform_time_series_analysis(df)

# Calculate commodity market factor
calculate_commodity_market_factor(df)
