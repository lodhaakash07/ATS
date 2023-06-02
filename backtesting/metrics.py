import numpy as np

def calculate_total_trades(portfolio):
    # Calculate and return the total number of trades from the portfolio
    trades = portfolio.get_trades()
    total_trades = len(trades)
    return total_trades

def calculate_max_drawdown(portfolio):
    # Calculate and return the maximum drawdown from the portfolio
    equity_curve = portfolio.get_equity_curve()
    max_drawdown = calculate_maximum_drawdown(equity_curve)
    return max_drawdown

def calculate_win_loss_ratio(portfolio):
    # Calculate and return the win/loss ratio from the portfolio
    trades = portfolio.get_trades()
    num_winning_trades = sum(trade.profit > 0 for trade in trades)
    num_losing_trades = sum(trade.profit < 0 for trade in trades)

    if num_losing_trades == 0:
        win_loss_ratio = float('inf')
    else:
        win_loss_ratio = num_winning_trades / num_losing_trades

    return win_loss_ratio

def calculate_sharpe_ratio(portfolio, risk_free_rate=0.0, annualized=True):
    # Calculate and return the Sharpe ratio from the portfolio
    returns = portfolio.get_returns()
    returns = np.asarray(returns)
    if annualized:
        returns = returns * np.sqrt(252)  # Assuming daily returns and 252 trading days in a year

    sharpe_ratio = (np.mean(returns) - risk_free_rate) / np.std(returns)

    return sharpe_ratio

def calculate_calmar_ratio(portfolio, risk_free_rate=0.0, annualized=True):
    # Calculate and return the Calmar ratio from the portfolio
    returns = portfolio.get_returns()
    returns = np.asarray(returns)
    if annualized:
        returns = returns * np.sqrt(252)  # Assuming daily returns and 252 trading days in a year

    max_drawdown = calculate_max_drawdown(portfolio)
    calmar_ratio = (np.mean(returns) - risk_free_rate) / abs(max_drawdown)

    return calmar_ratio

def calculate_sortino_ratio(portfolio, risk_free_rate=0.0, annualized=True):
    # Calculate and return the Sortino ratio from the portfolio
    returns = portfolio.get_returns()
    returns = np.asarray(returns)
    if annualized:
        returns = returns * np.sqrt(252)  # Assuming daily returns and 252 trading days in a year

    downside_returns = np.where(returns < 0, returns, 0)
    sortino_ratio = (np.mean(returns) - risk_free_rate) / np.std(downside_returns)

    return sortino_ratio

# Add more performance ratios, such as Sterling ratio, information ratio, etc.

