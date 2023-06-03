import pandas as pd
import numpy as np

def calculate_calmar_ratio(cumulative_returns, annualized_returns, max_drawdown):
    return annualized_returns / abs(max_drawdown)

def calculate_sortino_ratio(returns, risk_free_rate, target_return):
    downside_returns = returns - target_return
    downside_volatility = np.sqrt(np.mean(np.square(np.minimum(downside_returns, 0))))
    return (returns.mean() - risk_free_rate) / downside_volatility

def calculate_sharpe_ratio(returns, risk_free_rate):
    excess_returns = returns - risk_free_rate
    return excess_returns.mean() / excess_returns.std()

def calculate_information_ratio(returns, benchmark_returns):
    excess_returns = returns - benchmark_returns
    return excess_returns.mean() / excess_returns.std()

def calculate_alpha(returns, benchmark_returns, risk_free_rate):
    excess_returns = returns - risk_free_rate
    excess_benchmark_returns = benchmark_returns - risk_free_rate
    return np.mean(excess_returns) - (np.mean(excess_benchmark_returns) * np.mean(excess_returns)) / np.mean(excess_benchmark_returns ** 2)
"""
def calculate_beta(returns, benchmark_returns, risk_free_rate):
    excess_returns = returns - risk_free_rate
    excess_benchmark_returns = benchmark_returns - risk_free_rate
    return np.cov(excess_returns, excess_benchmark_returns)[0][1] / np.var(excess_benchmark_returns)
"""
def calculate_tracking_error(returns, benchmark_returns):
    excess_returns = returns - benchmark_returns
    return np.std(excess_returns)

def calculate_drawdown(returns):
    cumulative_returns = (1 + returns).cumprod()
    previous_peaks = cumulative_returns.cummax()
    drawdown = (cumulative_returns - previous_peaks) / previous_peaks
    return drawdown.min()

def calculate_metrics(returns, benchmark_returns=None, risk_free_rate=0.03, target_return=0.0):
    metrics = {}

    metrics['Total Returns'] = returns.sum()
    metrics['Annualized Returns'] = returns.mean() * 252
    metrics['Volatility'] = returns.std() * np.sqrt(252)
    metrics['Max Drawdown'] = calculate_drawdown(returns)
    metrics['Calmar Ratio'] = calculate_calmar_ratio(metrics['Total Returns'], metrics['Annualized Returns'], metrics['Max Drawdown'])
    metrics['Sortino Ratio'] = calculate_sortino_ratio(returns, risk_free_rate, target_return)
    metrics['Sharpe Ratio'] = calculate_sharpe_ratio(returns, risk_free_rate)

    if benchmark_returns is not None:
        metrics['Information Ratio'] = calculate_information_ratio(returns, benchmark_returns)
        metrics['Alpha'] = calculate_alpha(returns, benchmark_returns, risk_free_rate)
       # metrics['Beta'] = calculate_beta(returns, benchmark_returns, risk_free_rate)
        metrics['Tracking Error'] = calculate_tracking_error(returns, benchmark_returns)

    return metrics
