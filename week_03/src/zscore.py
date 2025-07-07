# Calculating Hedge ratio, spread, and Z-score
import numpy as np
import pandas as pd
import statsmodels.api as sm

def zscore_calc(data1, data2, window_size = 30):
    """Calculate the hedge ratio using linear regression."""
    # Ensure data is aligned
    data1, data2 = data1.align(data2, join='inner', axis=0)
    
    Y = data1["Close"]
    X = data2["Close"]

    #  Run a Linear Regression
    X = sm.add_constant(X)  # Add a constant term for the intercept
    model = sm.OLS(Y, X).fit()
    hedge_ratio = model.params.iloc[1]  # The slope coefficient is the hedge ratio
    intercept = model.params.iloc[0]  # The intercept
    
    spread = Y - (hedge_ratio * X.iloc[:, 1] + intercept)
    rolling_mean = spread.rolling(window=window_size).mean()
    rolling_std = spread.rolling(window=window_size).std()
    
    zscore = (spread - rolling_mean) / rolling_std
    print(zscore)
    result_df = pd.DataFrame({
        "Close_data1": Y,
        "Close_data2": X.iloc[:, 1],  # Remove constant
        "Spread": spread,
        "ZScore": zscore,
        "RollingMean": rolling_mean,
        "RollingStd": rolling_std
    },index=data1.index)

    return result_df, hedge_ratio, intercept
