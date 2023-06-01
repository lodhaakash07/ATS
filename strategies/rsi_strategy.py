import pandas as pd
from indicators.rsi import calculate_rsi

def rsi_strategy(data, rsi_window=14, slow_rsi_window=50):
    # Calculate RSI and slow RSI
    rsi = calculate_rsi(data, window=rsi_window)
    slow_rsi = calculate_rsi(data, window=slow_rsi_window)
    
    # Initialize the trading signals array
    signals = pd.Series(0, index=data.index)
    
    # Determine the trading signals based on the strategy rules
    signals[(rsi > 70) & (slow_rsi > 50) & (rsi > slow_rsi)] = 1  # Positive signal
    signals[(rsi < 30) & (slow_rsi < 50) & (rsi < slow_rsi)] = -1  # Negative signal
    
    return signals
