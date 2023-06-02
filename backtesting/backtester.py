from risk_management.transaction_cost import calculate_transaction_cost

class Backtester:
    def __init__(self, data):
        self.data = data
        self.portfolio = None

    def set_portfolio(self, portfolio):
        self.portfolio = portfolio

    def execute_trades(self, strategy):
        for i in range(len(self.data)):
            # Generate trading signals based on the strategy
            signal = strategy.generate_signal(self.data, i)

            # Execute trades based on the signal
            if signal == "BUY":
                self.execute_buy_order(self.data.iloc[i])

            elif signal == "SELL":
                self.execute_sell_order(self.data.iloc[i])

            # Check and enforce stop-loss
            portfolio_drawdown = calculate_portfolio_drawdown(self.portfolio)
            if portfolio_drawdown > 0.05:  # 5% drawdown threshold
                self.execute_stop_loss()

    def execute_stop_loss(self):
        # Execute stop-loss mechanism
        apply_stop_loss(self.portfolio)


    def execute_buy_order(self, row):
        # Execute a buy order
        symbol = row["Symbol"]
        price = row["Close"]
        quantity = self.calculate_position_size(symbol, price)
        transaction_costs = calculate_transaction_costs(quantity, price, transaction_rate)  # Use a predefined transaction rate
        self.portfolio.buy(symbol, price, quantity, transaction_costs)

    def execute_sell_order(self, row):
        # Execute a sell order
        symbol = row["Symbol"]
        price = row["Close"]
        quantity = self.portfolio.get_position_quantity(symbol)
        transaction_costs = calculate_transaction_costs(quantity, price, transaction_rate)  # Use a predefined transaction rate
        self.portfolio.sell(symbol, price, quantity, transaction_costs)
        
        
    def calculate_position_size(self, symbol, price):
        # Use the position sizing function from the position_sizing module
        position_size = calculate_position_size(self.portfolio, symbol, price)
        return position_size


    def calculate_portfolio_performance(self):
        # Calculate portfolio performance metrics
        total_returns = self.portfolio.calculate_total_returns()
        annualized_returns = self.portfolio.calculate_annualized_returns()
        drawdowns = self.portfolio.calculate_drawdowns()
        sharpe_ratio = self.portfolio.calculate_sharpe_ratio()

        # Print or return the calculated metrics as needed

    def generate_reports(self):
        # Calculate additional performance metrics
        max_drawdown = calculate_max_drawdown(self.portfolio)
        win_loss_ratio = calculate_win_loss_ratio(self.portfolio)

        # Generate reports and visualizations
        report = f"=== Performance Report ===\n"
        report += f"Total Trades: {self.portfolio.get_total_trades()}\n"
        report += f"Max Drawdown: {max_drawdown:.2%}\n"
        report += f"Win/Loss Ratio: {win_loss_ratio:.2f}\n"

        # Generate other reports and visualizations...

        print(report)