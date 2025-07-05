# Calculates Spread and Z-Score for two tickers and visualises the spread/z-score behaviour

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def calculate_zscore(df, window_size=30):
    
    spread = df.iloc[:, 0] - df.iloc[:, 1] #array
    mean = spread.rolling(window = window_size).mean() #array
    std = spread.rolling(window = window_size).std() #array

    zscore = (spread - mean)/std #array

    result = pd.DataFrame({
        'Spread': spread,
        'Z-Score': zscore
    },index = df.index)
    result.to_csv('data/zscore_data.csv')  # Save to CSV for future use
    return result

def plot_spread(zscore_df, entry_threshold, exit_threshold):
    
    import streamlit as st

    fig,ax = plt.subplots()
    zscore_df["Z-Score"].plot(ax=ax)
    ax.axhline(entry_threshold, color='green', linestyle='--')
    ax.axhline(-entry_threshold, color='green', linestyle='--')
    ax.axhline(exit_threshold, color='red', linestyle='--')
    ax.axhline(-exit_threshold, color='red', linestyle='--')
    ax.set_title("Z-Score of Spread")
    st.pyplot(fig)