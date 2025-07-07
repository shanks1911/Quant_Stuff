# Backtesting and calculating performance metrics for the strategy
import numpy as np

def backtest_strategy(signal_df, hedge_ratio, initial_capital):
    df = signal_df.copy()
    df["Ret_Y"] = np.log(df["Close_data1"] / df["Close_data1"].shift(1))
    df["Ret_X"] = np.log(df["Close_data2"] / df["Close_data2"].shift(1))

    df["Strategy_return"] = df["Position"].shift(1) * (df["Ret_Y"] - hedge_ratio * df["Ret_X"])
    # Capital growth
    df['cumulative_return'] = (1 + df['Strategy_return']).cumprod()
    df['portfolio_value'] = initial_capital * df['cumulative_return']
    df['pnl'] = df['portfolio_value'] - initial_capital

    return df