from indicators.bollinger_bands import calculate_bollinger_bands
import numpy as np

def bollinger_band_strategy(data, window=20, num_std=2):
    # Calculate the upper and lower bands using the calculate_bollinger_bands function
    print(data)
    upper_band, lower_band = calculate_bollinger_bands(data, window=window)
    
    # Calculate the moving average
    ma = data.rolling(window).mean()
    
    # Calculate the band width
    band_width = (upper_band - lower_band) / ma
    
    # Calculate the trend based on the position of the price relative to the bands
    trend = np.where(data > upper_band, -1, np.where(data < lower_band, 1, 0))
    
    # Calculate the trend direction based on the rate of change of the band width
    trend_direction = np.where(band_width.diff() > 0, 1, -1)
    
    # Generate trading signals based on the trend and trend direction
    signal = np.where((trend == -1) & (trend_direction == -1), -1,
                      np.where((trend == 1) & (trend_direction == 1), 1, 0))
    
    return signal
