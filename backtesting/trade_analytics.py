import pandas as pd
import matplotlib.pyplot as plt

def generate_trade_analytics(df):

    # Calculate the number of trades
    total_trades = len(df)
    profitable_trades = len(df[df['pnl'] > 0])
    unprofitable_trades = len(df[df['pnl'] < 0])
    
    # Calculate the average profit and loss
    average_profit = df[df['pnl'] > 0]['pnl'].mean()
    average_loss = df[df['pnl'] < 0]['pnl'].mean()

    # Calculate the profit factor
    profit_factor = df[df['pnl'] > 0]['pnl'].sum() / abs(df[df['pnl'] < 0]['pnl'].sum())

    # Calculate the win rate
    win_rate = profitable_trades / total_trades

    # Calculate the maximum drawdown
    df['previous_cumulative_pnl'] = df['cumulative_pnl'].shift(1).fillna(0)
    df['drawdown'] = df['cumulative_pnl'] - df['previous_cumulative_pnl']
    max_drawdown = df['drawdown'].min()

    # Calculate the recovery period for the maximum drawdown
    recovery_period = len(df[df['drawdown'] == max_drawdown])



    # Print trade analytics
    print('Total Trades:', total_trades)
    print('Profitable Trades:', profitable_trades)
    print('Unprofitable Trades:', unprofitable_trades)
    print('Average Profit:', average_profit)
    print('Average Loss:', average_loss)
    print('Profit Factor:', profit_factor)
    print('Win Rate:', win_rate)
    print('Max Drawdown:', max_drawdown)
    print('Recovery Period:', recovery_period)

    # Plot histogram of profits and losses
    plt.figure(figsize=(10, 6))
    plt.hist(df['pnl'], bins=20, color='blue', alpha=0.7)
    plt.title('Histogram of Profits and Losses')
    plt.xlabel('PnL')
    plt.ylabel('Frequency')
    plt.show()

    # Plot cumulative profits over time
    df['cumulative_pnl'].plot(figsize=(10, 6))
    plt.title('Cumulative Profits Over Time')
    plt.xlabel('Date')
    plt.ylabel('Cumulative PnL')
    plt.show()

    # Plot profits and losses by ticker
    df.groupby('ticker')['pnl'].sum().plot(kind='bar', figsize=(10, 6))
    plt.title('Profits and Losses by Ticker')
    plt.xlabel('Ticker')
    plt.ylabel('PnL')
    plt.show()

    # Return the DataFrame for further analysis
    return df
