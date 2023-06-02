from indicators.rsi import calculate_rsi
import numpy as np

def rsi_strategy(data, rsi_period=14, lookback_period=100, upper_threshold=70, lower_threshold=30):
    # Calculate RSI
    rsi = calculate_rsi(data, window=rsi_period)
    
    # Calculate dynamic thresholds
    upper_threshold = rsi.rolling(lookback_period).quantile(upper_threshold / 100)
    lower_threshold = rsi.rolling(lookback_period).quantile(lower_threshold / 100)
    
    # Calculate RSI divergence
    price_change = data.diff()
    rsi_change = rsi.diff()
    rsi_divergence = np.where((price_change > 0) & (rsi_change < 0), 1, 0)
    rsi_divergence = np.where((price_change < 0) & (rsi_change > 0), -1, rsi_divergence)
    
    # Generate trading signals
    signal = np.where(rsi > upper_threshold, -1, 0)
    signal = np.where(rsi < lower_threshold, 1, signal)
    signal += rsi_divergence
    
    return signal
