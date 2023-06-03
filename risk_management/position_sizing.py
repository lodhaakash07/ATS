import numpy as np
import pandas as pd
from scipy.optimize import minimize

class PositionSizer:
    def __init__(self, capital, risk_percentage):
        self.capital = capital
        self.risk_percentage = risk_percentage

    def calculate_position_size(self, data, toTrade):
      
        prices = data[toTrade].copy()
        returns = np.log(prices / prices.shift(1)).dropna()
        volatilities = returns.std()
        inv_volatilities = 1 / volatilities
        weights = inv_volatilities / inv_volatilities.sum()
        position_size = self.capital * weights
        position_sizes = {ticker: size for ticker, size in zip(toTrade, position_size)}

        # Return the position sizes
        return position_sizes

    def markov_position_size(self, data, toTrade):
        prices = data[toTrade].copy()
        
        returns = np.log(prices / prices.shift(1)).dropna()

        # Define the objective function for portfolio optimization
        def objective_function(weights):
            portfolio_returns = np.dot(returns, weights)
            portfolio_variance = np.dot(weights, np.dot(returns.cov(), weights))
            utility = portfolio_returns - 0.5 * self.risk_percentage * portfolio_variance
            return -np.sum(1 / utility)  # Use the inverse of utility as the objective

        # Define the constraint for portfolio weights summing up to 1
        constraint = {'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1}

        # Set the initial guess
        initial_weights = np.ones(len(toTrade)) / len(toTrade)


        bounds = [(0, 1) for _ in range(len(toTrade))]


        result = minimize(objective_function, initial_weights, method='SLSQP', constraints=constraint, bounds=bounds)


        optimal_weights = result.x

        # Calculate the position size based on the optimal weights and available capital
        position_size = self.capital * optimal_weights

        # Create a dictionary to store the ticker and corresponding position size
        position_sizes = {ticker: size for ticker, size in zip(toTrade, position_size)}

        return position_sizes