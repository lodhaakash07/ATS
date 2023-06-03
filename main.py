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
from backtesting.sensitivity_analysis import find_sensitivity
from utils.time_series_analysis import perform_time_series_analysis
from utils.get_market_factor import get_market_factor

import warnings
warnings.filterwarnings("ignore")

# Create the output folder if it doesn't exist
output_folder = 'output'
os.makedirs(output_folder, exist_ok=True)

global add_section

def add_section():
    print("------------------------")
    print()



# Load the data from the Excel file
file_path = 'data/raw/Commodities Data thru 18May23.xlsx'
df = load_commodities_data(file_path)


# Set the date column as the index
df.set_index('Dates', inplace=True)


print("Summary statistics for each assets")
perform_time_series_analysis(df)
add_section()

# Calculate commodity market factor
print("Commodity market factor")
cmf = get_market_factor(df)

print(add_section)


strategy = TA_Strategies(rsi_window=9, ma_short_period=3, ma_long_period=21, bb_window=20)

portfolio = Portfolio(initial_capital=1)

portfolio_cmf = Portfolio(initial_capital=1)

risk_percentage = 5


backtester = Backtester(df.copy(), strategy, risk_percentage, portfolio)
backtester_cmf = Backtester(cmf.copy(), strategy, risk_percentage, portfolio_cmf)

backtester.execute_trades("portfolio")
backtester_cmf.execute_trades("cmf")

# Trade analytics 
print('Trade analytics for the portfolio')
generate_trade_analytics(portfolio.trade_logs)
add_section()

print(' Trade Analytics for the Commodity Market Factor')
generate_trade_analytics(portfolio_cmf.trade_logs )
add_section()


matrics = calculate_metrics(portfolio.trade_logs['pnl'], portfolio_cmf.trade_logs['pnl'])

# Print the metrics
print('Comparing metics of the commodity return vs commodity factor returns')
for key, value in matrics.items():
    print(key + ':', value)

add_section()
    
# Sensitivity to market factors
common_index = portfolio.trade_logs.index.intersection(portfolio_cmf.trade_logs.index)
subset_returns = portfolio.trade_logs.loc[common_index, 'pnl']
subset_cmf_returns = portfolio_cmf.trade_logs.loc[common_index, 'pnl']


# Sector wise contribution

sector_mappings = pd.read_excel(file_path, sheet_name='Assets')
sector_mappings = dict(zip(sector_mappings['Commodity'], sector_mappings['Sector']))
portfolio.trade_logs['Sector'] = portfolio.trade_logs['ticker'].apply(lambda x: next((v for k, v in sector_mappings.items() if k in x), 'noMatching'))

# Calculate the sector-wise total PnL
sector_pnl = portfolio.trade_logs.groupby('Sector')['pnl'].sum()

total_pnl = portfolio.trade_logs['pnl'].sum()

sector_pnl = (sector_pnl / total_pnl) * 100

print('Sector-wise Contribution:')
print(sector_pnl)
add_section()