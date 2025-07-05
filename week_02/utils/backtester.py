# Logic
# Z-score > entry? → SHORT spread
# Z-score < -entry? → LONG spread
# Z-score reverses to near 0 → EXIT

# Daily spread change → PnL
# PnL → Update equity

import numpy as np
import pandas as pd

def backtest_strategy(zscore_df, entry_threshold, exit_threshold):
    position = 0  # 1 for long, -1 for short, 0 for neutral
    pnl = []  # List to store daily PnL
    equity = [100000] # Starting equity of $100,000. Stores daily equity values
    df = zscore_df.copy()  # Avoid modifying the original DataFrame
    df.dropna(subset=['Z-Score'], inplace=True)
    for i in range(1, len(df)):
        z = df['Z-Score'].iloc[i]
        prev_z = df['Z-Score'].iloc[i - 1]
        spread_change = df['Spread'].iloc[i] - df['Spread'].iloc[i - 1]
        # Check for entry/exit signals
        if position == 0:  # No open position
            if z > entry_threshold: # Short signal
                position = -1
            elif z < -entry_threshold:  # Long signal
                position = 1
        elif position == 1 and z > exit_threshold:
            position = 0  # Close long position
        elif position == -1 and z < -exit_threshold:
            position = 0
        
        # Calculate PnL for the day
        pnl.append(spread_change * position)
        equity.append(equity[-1] + position * spread_change)
        print(f"Day {i}: Z-Score = {z}, Spread Change = {spread_change}, Position = {position}, pnL = {pnl[-1]}, Equity = {equity[-1]}")
        
    results = {
            'pnl': sum(pnl),  # Total PnL 
            'equity_curve': pd.Series(equity, index=df.index)
        }
    return results