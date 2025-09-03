---
title: Derivatives Pricing & Risk Management System
sdk: docker
app_port: 8501
---

# Derivatives Pricing & Risk Management System

An institutional-quality software toolkit built in Python and C++ for pricing financial derivatives and analyzing their associated risks. This project showcases the implementation of complex financial theory into robust, high-performance code, presented in a professional, interactive web application.

### Core Features
- **Analytic Pricing:** Calculates prices for European Calls and Puts using the Black-Scholes-Merton formula.
- **Numerical Pricing:** Prices exotic, path-dependent options (e.g., Asian Options) using a Monte Carlo simulator.
- **C++ Performance:** The core Monte Carlo simulation engine is written in C++ and exposed to Python via pybind11 for a significant performance boost.
- **Risk Analysis:** Computes and displays all key Greeks (Delta, Gamma, Vega, Theta) for risk management.
- **Implied Volatility:** Includes a root-finding solver to calculate the implied volatility from a given market price.
- **Market Data Integration:** Fetches live options chain data from `yfinance` to plot the real-world Volatility Smile/Skew.
- **Interactive Dashboard:** A multi-tab Streamlit application provides a user-friendly interface for all analytics.

### Technical Stack
- **Primary Language:** Python
- **Performance Language:** C++
- **Python Libraries:** NumPy, SciPy, Streamlit, Matplotlib, yfinance, pandas
- **Binding Generator:** pybind11 for Python/C++ interoperability

### Performance Benchmark
The Monte Carlo simulation's performance was significantly improved by rewriting the core loop in C++.

| Simulator Version | Paths | Timesteps | Time Taken (s) | Speedup |
| :--- | :--- | :--- | :--- | :--- |
| Pure Python (NumPy) | 100,000 | 252 | 65.71 s | 1x |
| **C++ Accelerated (pybind11)** | **100,000** | **252** | **1.66 s** | **~40x** |

---
