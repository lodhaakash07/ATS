def rsi_strategy(df, rsi_period=14, lookback_period=100, upper_threshold=90, lower_threshold=10):
    # Calculate RSI
    df['RSI'] = talib.RSI(df['Close'], timeperiod=rsi_period)
    
    # Calculate dynamic thresholds
    df['UpperThreshold'] = df['RSI'].rolling(lookback_period).quantile(upper_threshold / 100)
    df['LowerThreshold'] = df['RSI'].rolling(lookback_period).quantile(lower_threshold / 100)
    
    # Calculate RSI divergence
    df['PriceChange'] = df['Close'].diff()
    df['RSIChange'] = df['RSI'].diff()
    df['RSIDivergence'] = np.where((df['PriceChange'] > 0) & (df['RSIChange'] < 0), 1, 0)
    df['RSIDivergence'] = np.where((df['PriceChange'] < 0) & (df['RSIChange'] > 0), -1, df['RSIDivergence'])
    
    # Generate trading signals
    df['Signal'] = 0
    df.loc[df['RSI'] > df['UpperThreshold'], 'Signal'] = -1
    df.loc[df['RSI'] < df['LowerThreshold'], 'Signal'] = 1
    df['Signal'] += df['RSIDivergence']
    
    # Apply signal lag
    df['Signal'] = df['Signal'].shift()
    
    return df
