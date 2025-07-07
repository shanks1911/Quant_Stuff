# generating signals based on z-score

import numpy as np
import pandas as pd

def signal_gen(zscore_df, entry_threshold=1.0, exit_threshold=0.3):
    df = zscore_df.copy()
    df.dropna(subset=['ZScore'], inplace=True)  # Ensure no NaN values in ZScore
    signals = []
    positions = []
    current_position = 0  # 1 for long, -1 for short, 0 for neutral

    for z in df['ZScore']:
        signal = 0  # Default no signal

        if current_position == 0:  # No open position
            if z > entry_threshold:  # Short signal: short Y, long X
                signal = -1
                current_position = -1
            elif z < -entry_threshold:  # Long signal: long Y, short X
                signal = 1
                current_position = 1
        else:
            if abs(z) < exit_threshold:
                signal = 0 # Exit signal
                current_position = 0

        signals.append(signal)
        positions.append(current_position)

    df["Signal"] = signals
    df["Position"] = positions

    return df