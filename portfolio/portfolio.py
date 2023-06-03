import pandas as pd

class Portfolio:
    def __init__(self, initial_capital):
        self.initial_capital = initial_capital
        self.capital = initial_capital
        self.positions = []
        self.trade_logs = []
        self.cumulative_pnl = [0]

    def add_positions(self, to_trade, position_sizes, data):

        # Iterate over the tickers to add positions
        for ticker in to_trade:
            entry_price = data.index

            position = {
                'date': data.index,
                'ticker': ticker,
                'entry_price': data[ticker],
                'amount': position_sizes[ticker],  # Use position size from position_sizes
                'exit_price': None  # Initialize exit price as None
            }

            self.positions.append(position)

            # Add the trade to trade_logs
            trade_log = {
                'date': data.index,
                'ticker': ticker,
                'entry_price': entry_price,
                'exit_price': None,  # Initialize exit price as None
                'amount': position_sizes[ticker]  # Use position size from position_sizes
            }

            self.trade_logs.append(trade_log)
    def remove_positions(self, data):
        self.update_pnl(data)
        updated_positions = []
        for position in self.positions:
            ticker = position['ticker']
            exit_price = data.loc[ticker]
            position['exit_price'] = exit_price

            # Update the trade log with exit price and date
            trade_log = {
                'date': data.index,
                'ticker': ticker,
                'entry_price': position['entry_price'],
                'exit_price': exit_price,
                'amount': position['amount']
            }
            self.trade_logs.append(trade_log)

        # Update the positions list by removing the closed positions
        self.positions = updated_positions


    def update_pnl(self, data):

        pnl = 0;

        for position in self.positions:
            ticker = position['ticker']
            entry_price = position['entry_price']
            exit_price = data.loc[ticker]
            amount = position['amount']

            # Calculate P&L
            pnl = pnl+((exit_price - entry_price) * amount)

            # Update cumulative P&L
        self.cumulative_pnl.append(pnl+self.cumulative_pnl[-1])

    def get_pnl(self, data):

        pnl = 0;

        for position in self.positions:
            ticker = position['ticker']
            entry_price = position['entry_price']
            exit_price = data.loc[ticker]
            amount = position['amount']

            # Calculate P&L
            pnl = pnl+((exit_price - entry_price) * amount)

            # Update cumulative P&L
        return pnl+self.cumulative_pnl[-1]