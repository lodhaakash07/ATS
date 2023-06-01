def moving_average_strategy(df, ma_short_period=20, ma_long_period=50):
    # Calculate the moving averages
    df['MA_Short'] = df['Close'].rolling(ma_short_period).mean()
    df['MA_Long'] = df['Close'].rolling(ma_long_period).mean()
    
    # Calculate the trend based on the moving averages
    df['Trend'] = np.where(df['MA_Short'] > df['MA_Long'], 1, -1)
    
    # Calculate the trend direction based on the rate of change of the moving averages
    df['TrendDirection'] = np.where(df['MA_Short'].diff() > 0, 1, -1)
    
    # Generate trading signals based on the trend and trend direction
    df['Signal'] = np.where((df['Trend'] == 1) & (df['TrendDirection'] == 1), 1, 
                            np.where((df['Trend'] == -1) & (df['TrendDirection'] == -1), -1, 0))
    
    return df
