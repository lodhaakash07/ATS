import pandas as pd
import csv
import numpy as np

class Portfolio:
    def __init__(self, initial_capital):
        self.initial_capital = initial_capital
        self.capital = initial_capital
        self.positions = []
        self.trade_logs = []
        self.portfolio_pnl = []

    def add_positions(self, to_trade, position_sizes, data):

        # Iterate over the tickers to add positions
        for ticker in to_trade:
            
            entry_price = data[ticker].tolist()[0]
      
            position = {
                'date': data.index[0],
                'ticker': ticker,
                'entry_price': data[ticker],
                'amount': position_sizes[ticker],  # Use position size from position_sizes
                'exit_price': None  # Initialize exit price as None
            }
            
            self.positions.append(position)

            

            # Add the trade to trade_logs
            
            trade_log = {
                'date': data.index[0],
                'ticker': ticker,
                'entry_price': entry_price,
                'exit_price': None,  # Initialize exit price as None
                'amount': position_sizes[ticker]  # Use position size from position_sizes
            }
            
            self.trade_logs.append(trade_log)


    def remove_positions(self, data):

        updated_positions = []



        for position in self.positions:
            ticker = position['ticker']
            exit_price = data.loc[:, ticker].tolist()[0]
            position['exit_price'] = exit_price
        
            # Update the trade log with exit price and date
            trade_log = {
                'date': data.index[0],
                'ticker': ticker,
                'entry_price': position['entry_price'].iloc[0],
                'exit_price': exit_price,
                'amount': position['amount']
            }
            
            self.trade_logs.append(trade_log)

        # Update the positions list by removing the closed positions
        self.positions = updated_positions

    def getCurrentTickers(self):
        currentTickers = {}
        for position in self.positions:

            currentTickers[position['ticker']] = 1 if position['amount'] > 0 else -1
        return currentTickers
    
    def processTradeLogs(self, name=""):
        # Convert the trade logs to a DataFrame
        self.trade_logs = pd.DataFrame(self.trade_logs)
        self.trade_logs.set_index('date', inplace=True)
        self.trade_logs.dropna(subset=['entry_price', 'exit_price'], inplace=True)
        # Calculate the profit or loss for each trade
        self.trade_logs['pnl'] = self.trade_logs['amount'] * (self.trade_logs['exit_price'] - self.trade_logs['entry_price'])
    
        # Calculate cumulative PnL
        self.trade_logs['cumulative_pnl'] = self.trade_logs['pnl'].cumsum()
        self.trade_logs.to_csv('data/processed/' + name + '_logs.csv')



    def updatePortfolioPnl(self, data):
        pnl = 0;
        for position in self.positions:
            exit_price = data.loc[:, position['ticker']].tolist()[0]
            entry_price = position['entry_price'][0],
            pnl = pnl + ((exit_price - entry_price) * position['amount'])

        pnl_update = {
                'date': data.index[0],
                'pnl': pnl,
        }
            
        self.portfolio_pnl.append(pnl_update)

    def processPortfolioPnl(self):
        # Convert the trade logs to a DataFrame
        self.portfolio_pnl = pd.DataFrame(self.portfolio_pnl)
        self.portfolio_pnl.set_index('date', inplace=True)
        # Calculate the profit or loss for each trade
        self.portfolio_pnl['returns'] = self.portfolio_pnl['pnl'].pct_change()
    
        # Calculate cumulative PnL
        self.portfolio_pnl['cumulative_pnl'] = self.portfolio_pnl['returns'].cumsum()