import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from bsm_model import black_scholes_merton
from payoff_diag import plot_payoff_diagram
from implied_volatility import implied_volatility
from monte_carlo import price_asian_option_mc

#  --- Streamlit App Layout ---

st.set_page_config(layout="wide")

st.title("Derivatives Pricing & Risk Management System")
st.markdown("An interactive toolkit for pricing and analyzing financial derivatives.")

tab1, tab2, tab3 = st.tabs(["European Option Analyzer", "Exotic Option Pricer", "Volatility Smile"])

# --- Tab 1: European Option Analyzer ---
with tab1:
    st.header("Black-Scholes-Merton Pricer")
    
    # Input parameters in a sidebar
    with st.sidebar:
        st.subheader("Model Inputs")
        option_type = st.radio("Option Type", ('Call', 'Put'))
        option_type = option_type.lower()  # Convert to lowercase for consistency
        S = st.number_input("Current Stock Price ($)", min_value=0.1, value=100.0, format="%.2f")
        EX = st.number_input("Strike Price ($)", min_value=0.1, value=100.0, format="%.2f")
        T_days = st.number_input("Time to Maturity (Days)", min_value=1, max_value=365, value=90)
        T = T_days / 365.0 # Convert days to years
        r = st.number_input("Risk-Free Interest Rate (%)", min_value=0.0, max_value=10.0, value=5.0) / 100
        sigma = st.number_input("Volatility (%)", min_value=0.1, max_value=100.0, value=20.0) / 100

    # Calculate price and greeks
    price, delta, gamma, vega, theta, rho = black_scholes_merton(S, EX, T, r, sigma, option_type)

    st.subheader("Pricing & Risk Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(label=f"{option_type.capitalize()} Price", value=f"${price:.3f}")
    with col2:
        st.metric(label="Delta", value=f"{delta:.4f}")
    with col3:
        st.metric(label="Gamma", value=f"{gamma:.4f}")
    with col4:
        st.metric(label="Vega", value=f"{vega:.4f}")
    
    col5, col6, col7, col8 = st.columns(4)
    with col5:
         st.metric(label="Theta (per day)", value=f"{theta:.4f}")
    with col6:
         st.metric(label="Rho", value=f"{rho:.4f}")
    
    st.divider()

    # Display Payoff Diagram
    st.subheader("Payoff Diagram at Expiration")
    payoff_fig = plot_payoff_diagram(S, EX, price, option_type)
    st.pyplot(payoff_fig)

    # In your app.py, inside the "with tab1:" block, after the payoff chart:

    st.divider()
    st.subheader("Implied Volatility Calculator")
    st.write("Find the volatility implied by a given market price.")

    # Get the market price from the user
    market_price_input = st.number_input("Enter Market Price of Option ($)", min_value=0.01, value=5.0, step=0.01, key="iv_input")

    # Calculate implied volatility
    iv = implied_volatility(market_price_input, S, EX, T, r, option_type)

    # Display the result
    if not np.isnan(iv):
        st.metric(label="Calculated Implied Volatility", value=f"{iv * 100:.2f}%")
    else:
        st.error("Could not find an implied volatility. The market price may be outside the valid no-arbitrage range.")

# --- Tab 2: Exotic Option Pricer ---
with tab2:
    st.header("Monte Carlo Simulator for Asian Options")
    st.markdown("This tool uses a C++ accelerated engine to price path-dependent Asian options.")

    # --- Simulation Parameters ---
    st.subheader("Simulation Parameters")
    num_simulations = st.slider("Number of Simulations", min_value=1000, max_value=100000, value=10000, step=1000)
    steps = st.slider("Time Steps per Path", min_value=50, max_value=500, value=252, step=1)

    if st.button("Run Monte Carlo Simulation"):
        with st.spinner(f"Running {num_simulations:,} simulations... This may take a moment."):
            # Call the pricing function using the correctly defined variables from the sidebar
            asian_price, paths = price_asian_option_mc(S, EX, T, r, sigma, num_simulations, steps, option_type)

            st.success("Simulation Complete!")
            
            # Display the result
            st.metric(f"Asian {option_type.capitalize()} Price", f"${asian_price:.3f}")

            # Display the plot of sample paths
            st.subheader("Sample of Simulated Price Paths")
            st.line_chart(paths)

# --- Tab 3: Volatility Smile ---
with tab3:
    st.header("Implied Volatility Smile/Skew")
    st.info("Work in Progress: This section will fetch live market data to calculate and plot the implied volatility for an options chain.")
    # Placeholder for future content
