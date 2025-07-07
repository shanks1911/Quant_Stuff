import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.data_loader import fetch_intraday_data
from src.zscore import zscore_calc 
from src.signal_gen import signal_gen
from src.backtesting import backtest_strategy

st.set_page_config(page_title = "Intraday Statistical Arbitrage Strategy Explorer", layout = "wide")

st.title("📈 Intraday StatArb Trading Simulator")
st.markdown("Simulate and evaluate a z-score-based pairs trading strategy using real intraday data.")

# Market toggle
market = st.radio("Select Market:", ["US", "India"], horizontal=True)

# Ticker input
if market == "India":
    ticker1 = st.text_input("Enter first stock (e.g., TCS.)", value="TCS")
    ticker2 = st.text_input("Enter second stock (e.g., INFY)", value="INFY")

    # Append .NS for NSE stocks
    ticker1 += ".NS"
    ticker2 += ".NS"

else:
    ticker1 = st.text_input("Enter first stock (e.g., AAPL)", value="AAPL")
    ticker2 = st.text_input("Enter second stock (e.g., MSFT)", value="MSFT")

# Sidebar for user inputs
st.sidebar.header("🔧 Strategy Configuration")

# Intraday Timeframe
timeframe = st.sidebar.selectbox("Timeframe (in minutes)", options=["1m", "5m", "15m"], index=1, help="Select the intraday timeframe for data analysis.")

if timeframe == "1m":
    max_period = 6
    max_rolling_window = 60
else :
    max_period = 50
    max_rolling_window = 200

# Date range input
period = int(st.sidebar.slider(
    "Select Period (number of days)",
    min_value=1,
    max_value=max_period,
    value=5,
    step=1,
    help="Choose the number of days for the analysis period."
))

end_date = st.sidebar.date_input("End Date", datetime.today())
start_date = st.sidebar.date_input("Start Date", end_date - timedelta(days=period))

# z-score parameters
rolling_window = int(st.sidebar.slider("Select Rolling Window (in bars)", min_value=10, max_value=max_rolling_window))
entry_threshold = float(st.sidebar.text_input("Entry Threshold", value="1.0", help="Z-score threshold for entering trades."))
exit_threshold = float(st.sidebar.text_input("Exit Threshold", value="0.3", help="Z-score threshold for exiting trades."))

# Capital and sizing
if market == "India":
    capital = st.sidebar.number_input("Initial Capital (₹)", min_value=10000, value=100000, step=1000)
else:
    capital = st.sidebar.number_input("Initial Capital ($)", min_value=1000, value=10000, step=100)
# sizing_method = st.sidebar.radio("Position Sizing", ["Fixed Lot", "Proportional"])

# # ML Toggle
# use_ml = st.sidebar.checkbox("🧠 Use ML Filter for Signal Confirmation")
# if use_ml:
#     model_choice = st.sidebar.selectbox("ML Model", ["Random Forest", "XGBoost", "Logistic Regression"])
#     st.sidebar.markdown("ℹ️ ML will predict spread direction using engineered features.")

# Submit
run_button = st.sidebar.button("🚀 Run Strategy")

# --- Main App Output (empty placeholder for now) ---
# if run_button:
#     data1 = fetch_intraday_data(ticker1, start_date, end_date, timeframe)
#     data2 = fetch_intraday_data(ticker2, start_date, end_date, timeframe)
#     st.info(f"Fetched data for {ticker1} and {ticker2} from {start_date} to {end_date} at {timeframe} intervals.")
#     st.dataframe(data1.head(), use_container_width=True)

if run_button:
    data1 = fetch_intraday_data(ticker1, start_date, end_date, timeframe)
    data2 = fetch_intraday_data(ticker2, start_date, end_date, timeframe)

    # Flatten column names if needed
    for df in [data1, data2]:
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [col[0] for col in df.columns]

    st.info(f"Fetched data for {ticker1} and {ticker2} from {start_date} to {end_date} at {timeframe} intervals.")

    zscore_df, hedge_ratio, intercept = zscore_calc(data1, data2, window_size=rolling_window)
    zscore_df = zscore_df.dropna(subset=['ZScore'])  # Drop rows with NaN Z-Score
    # st.dataframe(zscore_df, use_container_width=True)
    st.write(f"Hedge Ratio: {hedge_ratio:.4f}, Intercept: {intercept:.4f}")

    # Generate signals based on Z-Score
    signals_df = signal_gen(zscore_df, entry_threshold, exit_threshold)
    # st.header("📊 Generated Signals")
    # st.dataframe(signals_df, use_container_width=True)

    # Backtest the strategy
    backtest_df = backtest_strategy(signals_df, hedge_ratio, capital)
    st.header("💵 Cumulative Returns")
    st.line_chart(backtest_df['portfolio_value'], use_container_width=True)
    if market == "India":
        st.write(f"Final Portfolio Value: ₹{backtest_df['portfolio_value'].iloc[-1]:.2f}")
        st.write(f"Total PnL: ₹{backtest_df['portfolio_value'].iloc[-1] - capital}")
    else:
        st.write(f"Final Portfolio Value: ${backtest_df['portfolio_value'].iloc[-1]:.2f}")
        st.write(f"Total PnL: ${backtest_df['portfolio_value'].iloc[-1] - capital}")
    st.write(f"Total Trades Executed: {backtest_df['Signal'].abs().sum()}")
    st.header("📈 Backtest Results")
    st.dataframe(backtest_df[['Close_data1', 'Close_data2', 'Spread', 'ZScore', 'Signal', 'Position', 'portfolio_value']], use_container_width=True)

else:
    st.info("Configure strategy settings in the sidebar and click **Run Strategy**.")