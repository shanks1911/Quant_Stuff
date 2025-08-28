import numpy as np
import mc_engine_cpp  # type: ignore

def price_asian_option_mc(S0, K, T, r, sigma, num_simulations, steps, option_type='call'):
    """
    Prices an Asian option using the C++ accelerated Monte Carlo engine.

    Args:
        S0 (float): Initial stock price.
        K (float): Strike price.
        T (float): Time to maturity in years.
        r (float): Risk-free interest rate.
        sigma (float): Volatility.
        num_simulations (int): The number of paths to simulate.
        steps (int): The number of time steps in each path.
        option_type (str): 'call' or 'put'.

    Returns:
        tuple: A tuple containing the option price and a sample of paths for plotting.
    """
    payoffs = []
    paths_for_plotting = []

    # simulation loop
    for i in range(num_simulations):
        # C++ function to get a single path
        path = mc_engine_cpp.generate_single_path(S0, r, sigma, T, steps)
        
        #average price of the path (excluding the starting price S0)
        average_price = np.mean(path[1:])

        #payoff for this path
        if option_type == 'call':
            payoff = max(0, average_price - K)
        else: # 'put'
            payoff = max(0, K - average_price)
        
        payoffs.append(payoff)

        # small sample of paths to visualize later
        if i < 100: # Save the first 100 paths
            paths_for_plotting.append(path)

    # average payoff
    average_payoff = np.mean(payoffs)

    # Discount the average payoff back to the present value
    option_price = np.exp(-r * T) * average_payoff
    
    return option_price, np.array(paths_for_plotting).T

