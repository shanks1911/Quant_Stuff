Derivatives Pricing & Risk Management System

An institutional-quality software toolkit built in Python and C++ for pricing financial derivatives and analyzing their associated risks. This project showcases the implementation of complex financial theory into robust, high-performance code, presented in a professional, interactive web application.

Core Features
- Analytic Pricing: Calculates prices for European Calls and Puts using the Black-Scholes-Merton formula.
- Numerical Pricing: Prices exotic, path-dependent options (e.g., Asian Options) using a Monte Carlo simulator.
- C++ Performance: The core Monte Carlo simulation engine is written in C++ and exposed to Python via pybind11 for a significant performance boost.
- Risk Analysis: Computes and displays all key Greeks (Delta, Gamma, Vega, Theta) for risk management.
- Implied Volatility: Includes a root-finding solver to calculate the implied volatility from a given market price.
- Market Data Integration: Fetches live options chain data from yfinance to plot the real-world Volatility Smile/Skew.
- Interactive Dashboard: A multi-tab Streamlit application provides a user-friendly interface for all analytics.

Technical Stack

- Primary Language: Python
- Performance Language: C++ (C++17)
- Python Libraries: NumPy, SciPy, Streamlit, Matplotlib, yfinance
- Binding Generator: pybind11 for Python/C++ interoperability
- Tools: Git, GitHub, CMake (optional, for C++ build)

Project Architecture
The system is designed with a clear separation of concerns:

1. Analytics Core (Python/C++): A backend library containing modules for both the analytic (BSM) and numerical (Monte Carlo) engines. The most computationally intensive part—the path generation—is offloaded to a compiled C++ module for maximum speed.
2. Application UI (Streamlit): An interactive frontend that calls the backend analytics core to perform calculations and visualize results, allowing users to manipulate model parameters and see the impact in real-time.

Performance Benchmark
The Monte Carlo simulation's performance was significantly improved by rewriting the core loop in C++ and binding it to Python.

Simulator Version	Paths	Timesteps	Time Taken (s)	Speedup
Pure Python (NumPy)	100,000	252	~X.XX s	1x
C++ Accelerated (pybind11)	100,000	252	~Y.YY s	~50x
(Benchmark results are approximate and depend on the execution machine.)				

Setup and Installation
To run this application locally, please follow these steps:

1. Clone the repository:
git clone https://github.com/your-username/derivatives-pricing-system.git
cd derivatives-pricing-system

2. Set up a Python environment:

It is recommended to use a virtual environment.
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

3. Install Python dependencies:
pip install -r requirements.txt

4. Compile the C++ module:
You will need a C++ compiler (like g++ or Clang). The pybind11 headers are included via the pip install.

Usage
Once the setup is complete, run the Streamlit application:
streamlit run app.py

Open your web browser and navigate to the local URL provided by Streamlit (usually http://localhost:8501).