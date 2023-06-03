import numpy as np
import pandas as pd
from scipy.optimize import minimize

class PositionSizer:
    def __init__(self, capital, risk_percentage):
        self.capital = capital
        self.risk_percentage = risk_percentage

    def calculate_position_size(self, data, toTrade):
      
        # Extract the prices for the tickers in toTrade from the data
        prices = data[toTrade].copy()

        # Calculate the log returns of the prices
        returns = np.log(prices / prices.shift(1)).dropna()

        # Calculate the volatility of each asset
        volatilities = returns.std()

        # Calculate the inverse of the volatilities
        inv_volatilities = 1 / volatilities

        # Normalize the inverse volatilities so they sum up to 1
        weights = inv_volatilities / inv_volatilities.sum()
        # Calculate the position size based on the weights and available capital
        position_size = self.capital * weights

        # Create a dictionary to store the ticker and corresponding position size
        position_sizes = {ticker: size for ticker, size in zip(toTrade, position_size)}

        # Return the position sizes
        return position_sizes

    def markov_position_size(self, data, toTrade):
        # Extract the prices for the tickers in toTrade from the data
        prices = data[toTrade].copy()
        
        # Calculate the log returns of the prices
        returns = np.log(prices / prices.shift(1)).dropna()

        # Define the objective function for portfolio optimization
        def objective_function(weights):
            portfolio_returns = np.dot(returns, weights)
            portfolio_variance = np.dot(weights, np.dot(returns.cov(), weights))
            utility = portfolio_returns - 0.5 * self.risk_percentage * portfolio_variance
            return -np.sum(1 / utility)  # Use the inverse of utility as the objective

        # Define the constraint for portfolio weights summing up to 1
        constraint = {'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1}

        # Set the initial guess for portfolio weights
        initial_weights = np.ones(len(toTrade)) / len(toTrade)

        # Set the bounds for weights to be between 0 and 1
        bounds = [(0, 1) for _ in range(len(toTrade))]

        # Perform portfolio optimization using the scipy minimize function
        result = minimize(objective_function, initial_weights, method='SLSQP', constraints=constraint, bounds=bounds)

        # Get the optimal weights from the result
        optimal_weights = result.x

        # Calculate the position size based on the optimal weights and available capital
        position_size = self.capital * optimal_weights

        # Create a dictionary to store the ticker and corresponding position size
        position_sizes = {ticker: size for ticker, size in zip(toTrade, position_size)}

        # Return the position sizes
        return position_sizes