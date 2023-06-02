import pandas as pd

def calculate_rsi(data, window=14):
    # Convert the index to a standard datetime index
 
    diff = data.diff().dropna()
    up = diff * 0
    down = diff * 0
    up[diff > 0] = diff[diff > 0]
    down[diff < 0] = -diff[diff < 0]
    print(up)
    avg_gain = up.rolling(window=window, center = True).mean()
    avg_loss = down.rolling(window=window, center = True).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi
