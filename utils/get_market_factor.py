import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm

def get_market_factor(df):
    market_factor = []
    for index, row in df.iterrows():
        available_assets = row.count() - 1  # Exclude the 'Dates' column
        total_return = row.dropna().sum()
        weighted_average = total_return / available_assets
        market_factor.append(weighted_average)

    cmf = pd.DataFrame(market_factor)
    cmf.index = df.index
   
   
    # Plot the commodity market factor
    plt.figure(figsize=(10, 6))
    plt.plot(cmf.index, cmf)
    plt.xlabel('Date')
    plt.ylabel('Commodity Market Factor')
    plt.title('Commodity Market Factor - Weighted Average')
    plt.grid(True)
    plt.show()


    market_factor_statistics = cmf.describe()
    print('\nCommodity Market Factor - Descriptive Statistics:')
    print(market_factor_statistics)
    
    # Close the figure to release memory
    plt.close()

    return cmf

