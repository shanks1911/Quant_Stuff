#  Black Scholes Merton Model for Option Pricing
#  This module implements the Black-Scholes-Merton model for option pricing.
#  It includes functions to calculate the price of European call and put options.

import numpy as np
import scipy.stats as si

def black_scholes_merton(S, EX, T, r, sigma, option_type='call'):
    """
    Calculate the Black-Scholes-Merton price of a European call or put option.
    Parameters:
    S : float, Current stock price
    EX : float, Exercise price of the option
    T : float, Time to expiration in years
    r : float, Risk-free interest rate (annualized)
    sigma : float, Volatility of the underlying asset (annualized)
    option_type : str, 'call' for call option, 'put' for put option
    Returns:
    float, Price of the option
    """

    # Calculating d1(Value Factor) and d2(risk neutral probability factor)
    # d₁ = d₂ + σ√T

    d1 = (np.log(S / EX) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = (np.log(S / EX) + (r - 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))

    # Calculate the cumulative distribution function for d1 and d2
    N_d1 = si.norm.cdf(d1)
    N_d2 = si.norm.cdf(d2)

    # Calculate the option price based on the type
    if option_type.lower() == 'call':
        option_price = (S * N_d1) - (EX * np.exp(-r * T) * N_d2)
    elif option_type.lower() == 'put':
        option_price = (EX * np.exp(-r * T) * (1 - N_d2)) - (S * (1 - N_d1))
    else:
        raise ValueError("Invalid option type. Use 'call' or 'put'.")
    
    # Calculate Greeks
    delta = N_d1 if option_type.lower() == 'call' else N_d1 - 1
    gamma = si.norm.pdf(d1) / (S * sigma * np.sqrt(T))
    vega = S * si.norm.pdf(d1) * np.sqrt(T)
    theta = (-S * si.norm.pdf(d1) * sigma / (2 * np.sqrt(T)) - r * EX * np.exp(-r * T) * N_d2) if option_type.lower() == 'call' else (-S * si.norm.pdf(d1) * sigma / (2 * np.sqrt(T)) + r * EX * np.exp(-r * T) * (1 - N_d2))
    rho = EX * T * np.exp(-r * T) * N_d2 if option_type.lower() == 'call' else -EX * T * np.exp(-r * T) * (1 - N_d2)

    # Return the option price and Greeks
    return option_price, delta, gamma, vega, theta, rho