import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from bsm_model import black_scholes_merton
from payoff_diag import plot_payoff_diagram

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
        S = st.number_input("Current Stock Price ($)", min_value=0.1, value=100.0, step=0.50, format="%.2f")
        EX = st.number_input("Strike Price ($)", min_value=0.1, value=100.0, step=0.50, format="%.2f")
        T_days = st.slider("Time to Maturity (Days)", 1, 365, 90)
        T = T_days / 365.0 # Convert days to years
        r = st.slider("Risk-Free Interest Rate (%)", 0.0, 10.0, 5.0, 0.1) / 100
        sigma = st.slider("Volatility (%)", 1.0, 100.0, 20.0, 0.5) / 100

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


# --- Tab 2: Exotic Option Pricer ---
with tab2:
    st.header("Monte Carlo Simulator for Exotic Options")
    st.info("Work in Progress: This section will house the C++ accelerated Monte Carlo engine for pricing path-dependent options like Asian options.")
    # Placeholder for future content

# --- Tab 3: Volatility Smile ---
with tab3:
    st.header("Implied Volatility Smile/Skew")
    st.info("Work in Progress: This section will fetch live market data to calculate and plot the implied volatility for an options chain.")
    # Placeholder for future content
