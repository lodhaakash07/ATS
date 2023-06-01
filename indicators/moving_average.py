def calculate_moving_average(data, window, exponential=False):
    if exponential:
        return data.ewm(span=window, adjust=False).mean()
    else:
        return data.rolling(window).mean()


def calculate_kama(price_series, n=10, pow1=2, pow2=30):
    '''Calculate the Kaufman Adaptive Moving Average(KAMA) for a given series
    Parameters:
        price_series : pandas series, timeseries of price 
        n            : integer, lookback period
        pow1         : integer, fastest limit of exponential moving average window
        pow2         : integer, slowest limit of exponential moving average window
    Return:
        pandas series of KAMA indicator
    '''
    # Calculate the absolute price change (daily)
    delta = abs(price_series - price_series.shift())
    
    # Calculate the efficiency ratio = delta(n)/sum(n)
    efficiency_ratio = abs(price_series - price_series.shift(n)) / delta.rolling(n).sum()

    # Calculate the smoothing constant
    smoothing_constant = (efficiency_ratio * (2 / (pow1 + 1) - 2 / (pow2 + 1)) + 2 / (pow2 + 1)) ** 2

    # Calculate the KAMA
    kama = np.zeros_like(price_series)
    kama[:n] = price_series[:n]
    
    for i in range(n, len(price_series)):
        kama[i] = kama[i - 1] + smoothing_constant[i] * (price_series[i] - kama[i - 1])
    
    return pd.Series(kama, index=price_series.index)