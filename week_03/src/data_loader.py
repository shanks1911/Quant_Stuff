import numpy as np
import pandas as pd
import yfinance as yf

def fetch_intraday_data(ticker, start_date, end_date, timeframe):
    """
    Fetch intraday data for a given ticker and date range.
    
    Parameters:
    - ticker: Stock ticker symbol (e.g., 'AAPL', 'TCS.NS')
    - start_date: Start date for the data fetch
    - end_date: End date for the data fetch
    - timeframe: Timeframe for intraday data (e.g., '1m', '5m', '15m')
    
    Returns:
    - DataFrame with intraday data
    """
    # Fetch data using yfinance
    data = yf.download(ticker, start=start_date, end=end_date, interval=timeframe)
    # Ensure the index is a datetime index
    data.index = pd.to_datetime(data.index)
    
    if data.index.tz is None:
        data.index = data.index.tz_localize('UTC')
    
    if ticker.endswith('.NS'):
        # Convert to Indian time zone if ticker is NSE
        data.index = data.index.tz_convert('Asia/Kolkata')
    else:
        # Convert to US Eastern time zone for other markets
        data.index = data.index.tz_convert('America/New_York')
    
    # # Clean ticker (avoid invalid filename characters)
    # clean_ticker = ticker.replace(".", "_")
    # # Save the data to a CSV file
    # data.to_csv('week_03/data/{}_{}.csv'.format(clean_ticker, timeframe))

    return data

# if __name__ == "__main__":
#     # Example usage
#     ticker = "TCS.NS"
#     start_date = "2025-06-01"
#     end_date = "2025-06-30"
#     timeframe = "5m"
    
#     intraday_data = fetch_intraday_data(ticker, start_date, end_date, timeframe)