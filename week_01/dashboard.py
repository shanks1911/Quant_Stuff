import streamlit as st 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="S&P 500 Risk Dashboard",
    layout="wide"
)

st.title("📊 S&P 500 Risk Dashboard")
st.markdown("Explore volatility, Sharpe ratio, drawdown, and correlation between major sectors.")

# select ticker
tickers = ['XLK', 'XLF', 'XLE', 'XLV', 'XLY', 'XLI']

st.sidebar.header("Settings")

years = st.sidebar.slider("Select Years", 1, 10, 1)
curr_date = datetime.now().date()
year_ago = curr_date.replace(year=curr_date.year - years)

start_date = st.sidebar.date_input("Start Date", pd.to_datetime(year_ago))
end_date = st.sidebar.date_input("End Date", pd.to_datetime(curr_date))

st.sidebar.markdown("""
    **Sector ETF Legend:**
    - `XLK`: Technology  
    - `XLF`: Financials  
    - `XLE`: Energy  
    - `XLV`: Health Care  
    - `XLY`: Consumer Discretionary  
    - `XLI`: Industrials  
    """)

# Get Data
# @st.cache_data is used to cache the data for faster loading. it caches information like the dataframe, so it doesn't have to be reloaded every time the user interacts with the app.

def get_data():
    df =  yf.download(tickers, start=start_date, end=end_date, auto_adjust=True)
    if isinstance(df.columns, pd.MultiIndex):
        return df['Close']  # Auto-adjusted closing prices
    else:
        return df  # Already flattened structure

# Adjusted Close is the closing price after adjusting for dividends and stock splits.
# It gives the most accurate view of returns over time — essential for financial analysis and backtesting.

prices = get_data()
prices.to_csv('prices.csv')  # Save prices to CSV for reference

from metrics import log_returns
log_ret = log_returns(prices)

from metrics import volatility
vol = volatility(log_ret)

from metrics import sharpe_ratio
sharpe = sharpe_ratio(log_ret)

from metrics import drawdown
dd = drawdown(prices)

tabs = st.tabs(["📁 Data", "🔁 Log Returns", "📉 Volatility", "⚖️ Sharpe Ratio", "🧨 Drawdown", "🔗 Correlation"])

with tabs[0]:
    st.subheader("📁 Data with Adjusted Closing Prices")
    st.line_chart(prices, use_container_width=True)
    st.dataframe(prices)
    

with tabs[1]:
    st.subheader("🔁 Daily Log Returns")
    st.dataframe(log_ret.tail(10))  # Display last 10 rows of log returns
    st.line_chart(log_ret, use_container_width=True)

with tabs[2]:
    st.subheader("📉 Volatility (20-day Rolling Standard Deviation)")
    st.line_chart(vol, use_container_width=True)

with tabs[3]:
    st.subheader("⚖️ Sharpe Ratio (20-day Rolling)")
    st.line_chart(sharpe, use_container_width=True)

with tabs[4]:
    st.subheader("🧨 Drawdown (Peak to Trough)")
    st.line_chart(dd, use_container_width=True)

with tabs[5]:
    st.subheader("🔗 Correlation Matrix of Sectors")
    fig, ax = plt.subplots()
    sns.heatmap(prices.corr(), annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)