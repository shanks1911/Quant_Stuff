import numpy as np
import pandas as pd
import streamlit as st

from utils.data_loader import load_price_data
from utils.indicator import calculate_zscore, plot_spread
from utils.backtester import backtest_strategy
from utils.ml_model import ml_predict_spread

st.set_page_config(page_title="StatArb Strategy Explorer", layout="wide")

st.title("📉 Statistical Arbitrage Strategy Explorer")
st.write("Compare two assets using Z-score spreads, backtest trades, and apply ML to forecast spread direction.")

#  User Inputs
ticker1 = st.text_input("Enter first asset ticker (e.g., AAPL):", "AAPL")
ticker2 = st.text_input("Enter second asset ticker (e.g., MSFT):", "MSFT")

start_date = st.date_input("Start Date")
end_date = st.date_input("End Date")
window = st.slider("Rolling Window Size", min_value=10, max_value=120, value=30)

entry_threshold = float(st.text_input("Entry Threshold", value="1.0"))
exit_threshold = float(st.text_input("Exit Threshold", value="0.3"))

if st.button("Run Analysis"):
    data = load_price_data(ticker1, ticker2, start_date, end_date)
    zscore_df = calculate_zscore(data, window_size=window)
    st.subheader("Z-Score Spread Chart")
    plot_spread(zscore_df, entry_threshold, exit_threshold)

    st.subheader("📊 Backtest")
    result = backtest_strategy(zscore_df, entry_threshold, exit_threshold)
    st.write("### Backtest Summary")
    st.write(f"Total PnL: ${result['pnl']:.2f}")
    print(result["equity_curve"])
    st.line_chart(result['equity_curve'], use_container_width=True)

    st.subheader("🧠 ML Prediction")
    st.write(ml_predict_spread(zscore_df))