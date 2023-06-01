def bollinger_band_strategy(df, window=20, num_std=2):
    # Calculate the moving average and standard deviation
    df['MA'] = df['Close'].rolling(window).mean()
    df['Std'] = df['Close'].rolling(window).std()
    
    # Calculate the upper and lower bands
    df['UpperBand'] = df['MA'] + num_std * df['Std']
    df['LowerBand'] = df['MA'] - num_std * df['Std']
    
    # Calculate the band width
    df['BandWidth'] = (df['UpperBand'] - df['LowerBand']) / df['MA']
    
    # Calculate the trend based on the position of the price relative to the bands
    df['Trend'] = np.where(df['Close'] > df['UpperBand'], -1, 
                           np.where(df['Close'] < df['LowerBand'], 1, 0))
    
    # Calculate the trend direction based on the rate of change of the band width
    df['TrendDirection'] = np.where(df['BandWidth'].diff() > 0, 1, -1)
    
    # Generate trading signals based on the trend and trend direction
    df['Signal'] = np.where((df['Trend'] == -1) & (df['TrendDirection'] == -1), -1, 
                            np.where((df['Trend'] == 1) & (df['TrendDirection'] == 1), 1, 0))
    
    return df
