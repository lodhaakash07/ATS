#!/bin/bash

# Create the build directory if it doesn't exist
mkdir -p build

# Specify the files to copy with their relative paths
files=(
  "backtesting/backtester.py"
  "backtesting/metrics.py"
  "backtesting/trade_analytics.py"
  "backtesting/sensitivity_analysis.py"
  "indicators/bollinger_bands.py"
  "indicators/moving_average.py"
  "indicators/rsi.py"
  "portfolio/portfolio.py"
  "risk_management/position_sizing.py"
  "strategies/ta_strategy.py"
  "utils/data_loader.py"
  "utils/get_market_factor.py"
  "utils/time_series_analysis.py"
  "main.py",
  "data/raw/Commodities Data thru 18May23.xlsx",
  "data/processed"
  "environment.sh"
  "README.md"
  "requirement.tx"
)

# Loop through the files and copy them to the build directory while maintaining the directory structure
for file in "${files[@]}"; do
  mkdir -p "build/$(dirname "$file")"
  cp "$file" "build/$file"
done

echo "Files copied to build directory"
