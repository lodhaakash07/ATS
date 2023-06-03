from risk_management.transaction_cost import calculate_transaction_cost
from risk_management.position_sizing import PositionSizer
from strategies.ta_strategy import TA_Strategies
import pandas as pd

class Backtester:
    def __init__(self, data, strategy, risk_percentage, portfolio):
        self.data = data
        self.strategy = strategy
        self.portfolio = portfolio
        self.signal = pd.DataFrame(index=data.index)
        self.risk_percentage = risk_percentage
        self.position_sizer = PositionSizer(self.portfolio.capital, self.risk_percentage)


    def execute_trades(self):

        # Generate the signal for trade
        for column in self.data.columns:
            # Extract the price for the current commodity
            price = self.data[column]

            # Generate trading signals based on the TA strategy
            signal = self.strategy.generate_signal(price)
            
            self.signal[column] = signal
        
        self.signal.to_csv('1.csv') 
        
        for index, row in self.signal.iterrows():
            # extrct columns for which the value is non-zero
            to_trade = row[row != 0].index.tolist()
           
                
        
            if to_trade:
                # Check if these tickers are already trading in the portfolio
                isNewTrade = False
                for ticker in to_trade:
                    if ticker not in self.portfolio.positions:
                        self.portfolio.remove_positions(self.data.loc[index, :])
                        position_size = self.position_sizer.calculate_position_size(self.data.loc[:index, ], to_trade)
                        self.portfolio.add_positions(to_trade, position_size, self.data.loc[index, :])
                        isNewTrade = True
                        break
                if not isNewTrade:
                    self.portfolio.update_pnl(self.data.loc[index, :])

     
        print(self.portfolio.cumulative_pnl[-1])