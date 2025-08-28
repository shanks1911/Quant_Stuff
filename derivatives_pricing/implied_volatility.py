from scipy.optimize import brentq
import numpy as np
from bsm_model import black_scholes_merton

def implied_volatility(market_price, S, EX, T, r, option_type='call'):
    """
    Calculates the implied volatility of an option using the brentq root-finder.

    Args:
        market_price (float): The current market price of the option.
        All other args are the same as the BSM function.

    Returns:
        float: The implied volatility (as a decimal, e.g., 0.20 for 20%).
    """
    # Error Function
    def objective_function(sigma):
        """
        This function calculates the difference between the BSM price (for a given sigma) and the actual market price.
        The root-finder's goal is to make this function return 0.
        """
        price, _, _, _, _, _= black_scholes_merton(S, EX, T, r, sigma, option_type)
        return price - market_price
    
    # Use brentq to find the root of the objective function
    try:
        # Search for volatility between a very small number and 500%
        implied_vol = brentq(objective_function, 1e-6, 5.0)
    except ValueError:
        
        # If brentq fails to find a root (e.g., f(a) and f(b) have the same sign),
        # we don't crash. We gracefully return NaN.
        implied_vol = np.nan
    
    return implied_vol