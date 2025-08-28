import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from implied_volatility import implied_volatility

def plot_volatility_smile(ticker, S, T, r):
    """
    Fetches options chain data for a given ticker, calculates implied volatility
    for each option, and plots the resulting volatility smile.

    Args:
        ticker (str): The stock ticker (e.g., 'AAPL').
        S (float): The current stock price, used for IV calculation.
        T (float): Time to maturity in years.
        r (float): Risk-free interest rate.

    Returns:
        matplotlib.figure.Figure: The figure object for the plot, or None if data cannot be fetched.
    """
    try:
    
        stock = yf.Ticker(ticker)
        
        # first available options expiration date
        exp_date = stock.options[0]
        
        # options chain for that expiration date
        opt_chain = stock.option_chain(exp_date)
        calls = opt_chain.calls
        puts = opt_chain.puts

    except IndexError:
        return None

    # Calculate Implied Volatility for both calls and puts
    calls['impliedVolatility'] = calls.apply(
        lambda row: implied_volatility(row['lastPrice'], S, row['strike'], T, r, 'call'),
        axis=1
    )
    puts['impliedVolatility'] = puts.apply(
        lambda row: implied_volatility(row['lastPrice'], S, row['strike'], T, r, 'put'),
        axis=1
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Filter out rows where IV calculation failed (returned NaN)
    valid_calls = calls.dropna(subset=['impliedVolatility'])
    valid_puts = puts.dropna(subset=['impliedVolatility'])

    ax.scatter(valid_calls['strike'], valid_calls['impliedVolatility'] * 100, label='Calls', color='green', marker='^')
    ax.scatter(valid_puts['strike'], valid_puts['impliedVolatility'] * 100, label='Puts', color='red', marker='v')
    
    ax.set_xlabel('Strike Price ($)')
    ax.set_ylabel('Implied Volatility (%)')
    ax.set_title(f'Volatility Smile for {ticker.upper()} (Exp: {exp_date})')
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.6)
    
    # Add a vertical line for the current stock price
    ax.axvline(x=S, color='blue', linestyle='--', label=f'Current Price: ${S:.2f}')
    ax.legend()

    return fig

