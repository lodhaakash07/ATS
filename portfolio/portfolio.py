import pandas as pd
import csv
import numpy as np

class Portfolio:
    def __init__(self, initial_capital):
        self.initial_capital = initial_capital
        self.capital = initial_capital
        self.positions = []
        self.trade_logs = []

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
                'entry_price': position['entry_price'],
                'exit_price': exit_price,
                'amount': position['amount']
            }
            print(trade_log)
            self.trade_logs.append(trade_log)

        # Update the positions list by removing the closed positions
        self.positions = updated_positions

    def getCurrentTickers(self):
        currentTickers = {}
        for position in self.positions:

            currentTickers[position['ticker']] = 1 if position['amount'] > 0 else -1
        return currentTickers


    