import numpy as np
import yfinance as yf

def log_returns(prices):
    '''Calculate log returns from prices. Log returns are preferred in finance as they are time-additive and can be used for continuous compounding.'''
    '''log returns tell us how much the price has changed in percentage terms, accounting for compounding effects.'''
    log_ret = np.log(prices / prices.shift(1)).dropna()
    return log_ret

def volatility(log_ret):
    '''Calculate rolling volatility using a 20-day window and annualize it by multiplying by the square root of 252 (trading days in a year).'''
    '''higher volatility indicates higher risk, while lower volatility suggests more stable returns.'''
    rolling_vol = log_ret.rolling(window = 20).std() * np.sqrt(252)
    return rolling_vol

def sharpe_ratio(log_ret):
    '''Calculate the Sharpe Ratio using a 20-day rolling window. The Sharpe Ratio measures risk-adjusted return, indicating how much excess return is received for the extra volatility endured.'''
    '''A higher Sharpe Ratio indicates better risk-adjusted performance.'''
    sharpe = (log_ret.rolling(window=20).mean() / log_ret.rolling(window=20).std()) * np.sqrt(252)
    return sharpe

def drawdown(prices):
    '''Calculate the drawdown as the percentage decline from the peak price. Drawdown measures the decline from a historical peak in prices, indicating the risk of loss.'''
    '''A larger drawdown indicates a more significant risk of loss, while a smaller drawdown suggests a more stable investment.'''
    peak = prices.cummax()
    drawdown = (prices - peak) / peak
    return drawdown