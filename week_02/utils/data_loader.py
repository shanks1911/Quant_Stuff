# Loads price data for two tickers using yfinance

def load_price_data(ticker1, ticker2, start, end):
    import pandas as pd
    import yfinance as yf
    data = yf.download([ticker1, ticker2], start=start, end=end, auto_adjust=True)['Close']
    # data.to_csv('data/price_data.csv')  # Save to CSV for future use
    return data.dropna()