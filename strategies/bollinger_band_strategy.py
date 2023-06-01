import pandas as pd
from indicators.bollinger_bands import calculate_bollinger_bands

def bollinger_band_strategy(data, window=20):
    # Calculate Bollinger Bands
    upper_band, lower_band = calculate_bollinger_bands(data, window=window)
    
    # Compute the difference between upper and lower bands
    band_width = upper_band - lower_band
    
    # Initialize the trading signals array
    signals = pd.Series(0, index=data.index)
    
    # Determine the trading signals based on the strategy rules
    signals[band_width.diff() > 0] = 1  # Positive signal (expanding bands)
    signals[band_width.diff() < 0] = -1  # Negative signal (contracting bands)
    
    return signals
