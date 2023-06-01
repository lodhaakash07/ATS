#!/bin/bash

# Create data directory and subdirectories
mkdir data
cd data
mkdir raw processed
cd ..

# Create strategies directory
mkdir strategies

# Create risk management directory and files
mkdir risk_management
touch risk_management/position_sizing.py
touch risk_management/stop_loss.py

# Create indicators directory
mkdir indicators

# Create execution directory and files
mkdir execution
touch execution/broker.py
touch execution/order.py

# Create backtesting directory and files
mkdir backtesting
touch backtesting/backtest.py
touch backtesting/metrics.py

# Create live trading directory
mkdir live_trading

# Create utils directory and files
mkdir utils
touch utils/data_loader.py
touch utils/logger.py

# Create tests directory
mkdir tests

# Create config.py file
touch config.py

# Create requirements.txt file
touch requirements.txt

# Create README.md file
touch README.md

# Create main.py file
touch main.py

# Provide a summary of the created project structure
echo "Trading system project structure has been created successfully."

# Change back to the original directory
cd ..
