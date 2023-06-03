from risk_management.transaction_cost import calculate_transaction_cost
from strategies.ta_strategy import TA_Strategies

class Backtester:
    def __init__(self, data, strategy, portfolio):
        self.data = data
        self.strategy = strategy
        self.portfolio = portfolio



    def execute_trades(self, strategy:TA_Strategies):
        for column in self.data.columns:
            # Extract the price for the current commodity
            price = self.data[column]

            # Generate trading signals based on the TA strategy
            signal = self.strategy.generate_signal(price)
            
            self.data[f'{column}_Signal'] = signal