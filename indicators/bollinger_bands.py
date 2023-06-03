def calculate_bollinger_bands(data, window):
    # Calculate the rolling mean (SMA) using the window size
    sma = data.rolling(window).mean()
    
    # Calculate the rolling standard deviation (std) using the window size
    std = data.rolling(window).std()
    
    # Calculate the upper band as the SMA plus 2 times the std
    upper_band = sma + 2 * std
    
    # Calculate the lower band as the SMA minus 2 times the std
    lower_band = sma - 2 * std
    
    return upper_band, lower_band, sma
