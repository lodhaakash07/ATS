from risk_management.transaction_cost import calculate_transaction_cost
from risk_management.position_sizing import PositionSizer
from strategies.ta_strategy import TA_Strategies
import pandas as pd
import matplotlib.pyplot as plt
from backtesting.trade_analytics import generate_trade_analytics


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
        
        self.signal.to_csv('10.csv')
        for index, row in self.signal.iterrows():
            # extrct columns for which the value is non-zero
            to_trade = row[row != 0].index.tolist()
           

            if to_trade:
                # Check if these tickers are already trading in the portfolio
                      
                currentPositions = self.portfolio.getCurrentTickers()

                rebalance = False
                for ticker in to_trade:
                    if (not currentPositions.get(ticker)):
                        rebalance = True
                    else:
                        if pd.isna(row[ticker]) == False and int(currentPositions[ticker]) != int(row[ticker]):
                            rebalance = True;
                
                if rebalance:
                    for key, value in currentPositions.items():
                        if key not in to_trade:
                            to_trade.append(key)

                    if(currentPositions):
                        self.portfolio.remove_positions(self.data.loc[[index], :])
                    position_size = self.position_sizer.calculate_position_size(self.data.loc[:index, ], to_trade)
                    print(position_size)
               
                    for temp in to_trade:
                        position_size[temp] = position_size[temp] * row[temp]
                    self.portfolio.add_positions(to_trade, position_size, self.data.loc[[index], :])
        
        
        self.portfolio.remove_positions(self.data.iloc[[self.data.shape[0] - 1], :])
        generate_trade_analytics(self.portfolio.trade_logs)

       