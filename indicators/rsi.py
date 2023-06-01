import pandas as pd

def calculate_rsi(data, window=14):
    diff = data.diff().dropna()
    up = diff * 0
    down = diff * 0
    up[diff > 0] = diff[diff > 0]
    down[diff < 0] = -diff[diff < 0]
    avg_gain = up.rolling(window).mean()
    avg_loss = down.rolling(window).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi
