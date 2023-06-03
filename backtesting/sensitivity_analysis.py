import statsmodels.api as sm

def find_sensitivity(returns, market_factor):

    model = sm.OLS(returns, market_factor)
    results = model.fit()

    coefficients = results.params

    sensitivity_to_market = coefficients['market_factor']

    return sensitivity_to_market
