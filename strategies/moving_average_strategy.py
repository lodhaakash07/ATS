import pandas as pd
from indicators.moving_average import calculate_moving_average

def moving_average_strategy(data, fast_window=50, slow_window=200):
    # Calculate the fast and slow moving averages
    fast_ma = calculate_moving_average(data, window=fast_window)
    slow_ma = calculate_moving_average(data, window=slow_window)
    
    # Compute the difference between fast and slow moving averages
    ma_diff = fast_ma - slow_ma
    
    # Initialize the trading signals array
    signals = pd.Series(0, index=data.index)
    
    # Determine the trading signals based on the strategy rules
    signals[ma_diff > 0] = 1  # Positive signal
    signals[ma_diff < 0] = -1  # Negative signal
    
    return signals
