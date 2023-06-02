import pandas as pd
import matplotlib.pyplot as plt
from utils.data_loader import load_commodities_data
from strategies.moving_average_strategy import moving_average_strategy
from strategies.rsi_strategy import rsi_strategy
from strategies.bollinger_band_strategy import bollinger_band_strategy
from portfolio.portfolio import Portfolio
from backtesting.backtester import Backtester

def perform_time_series_analysis(df):
    for column in df.columns:
        # Calculate the moving average
        ma = df[column].rolling(window=20).mean()
        
        # Calculate the trend direction based on the rate of change of the moving average
        trend_direction = df[column].diff().apply(lambda x: 1 if x > 0 else -1)
        
        # Print numerical statistics
        mean = df[column].mean()
        std = df[column].std()
        autocorr = df[column].autocorr()
        print(f'Commodity: {column}')
        print(f'Mean: {mean:.2f}')
        print(f'Standard Deviation: {std:.2f}')
        print(f'Autocorrelation: {autocorr:.2f}')
        print('\n')
        
        # Plot the original, moving average, and trend direction
        plt.figure(figsize=(12, 8))
        plt.subplot(311)
        plt.plot(df.index, df[column], label='Original')
        plt.legend(loc='best')
        plt.subplot(312)
        plt.plot(df.index, ma, label='Moving Average')
        plt.legend(loc='best')
        plt.subplot(313)
        plt.plot(df.index, trend_direction, label='Trend Direction')
        plt.legend(loc='best')
        plt.tight_layout()
        plt.title(f'{column} - Time Series Analysis')
        plt.show()


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

# Iterate over each commodity
for column in df.columns:
    # Extract the price series for the current commodity
    price_series = df[column]

    # Generate trading signals based on the moving average strategy for the current commodity
    ma_signals = moving_average_strategy(price_series, price_series)

    # Generate trading signals based on the RSI strategy for the current commodity
    rsi_signals = rsi_strategy(price_series, column)

    # Generate trading signals based on the Bollinger Bands strategy for the current commodity
    bb_signals = bollinger_band_strategy(price_series)

    # Combine the signals into a single column
    signals = ma_signals['Signal'] + rsi_signals['Signal'] + bb_signals['Signal']
    
    # Add the signals to the dataset
    df[f'{column}_Signal'] = signals



# Create an instance of the Backtester class
backtester = Backtester(df)

# Set the portfolio
backtester.set_portfolio(Portfolio())


# Generate reports and visualizations
#backtester.generate_reports()
