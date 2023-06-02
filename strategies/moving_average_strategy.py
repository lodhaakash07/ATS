import numpy as np
from indicators.moving_average import calculate_moving_average
import statsmodels.api as sm

def moving_average_strategy(data, window=20):
    # Perform time series decomposition on the data
    decomposition = sm.tsa.seasonal_decompose(data, model='additive')

    # Use trend component to set the short and long periods dynamically
    trend = decomposition.trend
    short_period = len(trend) // 10  # Set the short period as a fraction of the trend length
    long_period = len(trend) // 5  # Set the long period as a larger fraction of the trend length

    # Calculate the moving averages using the updated periods
    ma_short = calculate_moving_average(data, short_period)
    ma_long = calculate_moving_average(data, long_period)

    # Calculate the trend based on the moving averages
    trend = np.where(ma_short > ma_long, 1, -1)

    # Calculate the trend direction based on the rate of change of the moving averages
    trend_direction = np.where(ma_short.diff() > 0, 1, -1)

    # Generate trading signals based on the trend and trend direction
    signal = np.where((trend == 1) & (trend_direction == 1), 1,
                      np.where((trend == -1) & (trend_direction == -1), -1, 0))

    return signal
