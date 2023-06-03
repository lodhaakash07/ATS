from indicators.rsi import calculate_rsi
from indicators.moving_average import calculate_moving_average
from indicators.bollinger_bands import calculate_bollinger_bands
import numpy as np

class TA_Strategies:
    def __init__(self, rsi_window=9, ma_short_period=3, ma_long_period=21, bb_window=20):
        self.rsi_window = rsi_window
        self.ma_short_period = ma_short_period
        self.ma_long_period = ma_long_period
        self.bb_window = bb_window

    def generate_signal(self, data):
        rsi = calculate_rsi(data, window=self.rsi_window)
        long_momentum = calculate_moving_average(rsi, period=self.ma_long_period, type="weighted")
        short_momentum = calculate_moving_average(rsi, period=self.ma_short_period, type="ema")
        bollinger_band = calculate_bollinger_bands(data, window=self.bb_window)

        # Generate trading signals based on the conditions
        signal = np.zeros_like(data)

        # Go long if the conditions are met
        long_conditions = (rsi < 50) & (long_momentum < 50) & (short_momentum > long_momentum) & (data > bollinger_band[2])
        signal[long_conditions] = 1

        # Go short if the conditions are met
        short_conditions = (rsi > 50) & (long_momentum > 50) & (long_momentum < short_momentum) & (data < bollinger_band[2])
        signal[short_conditions] = -1

        return signal
