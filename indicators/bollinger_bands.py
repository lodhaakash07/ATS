import pandas as pd

def calculate_bollinger_bands(data, window=20):
    rolling_mean = data.rolling(window).mean()
    rolling_std = data.rolling(window).std()
    upper_band = rolling_mean + 2 * rolling_std
    lower_band = rolling_mean - 2 * rolling_std
    return upper_band, lower_band
