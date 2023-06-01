def calculate_moving_average(data, window, exponential=False):
    if exponential:
        return data.ewm(span=window, adjust=False).mean()
    else:
        return data.rolling(window).mean()
