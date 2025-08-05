import numpy as np
import matplotlib.pyplot as plt

def plot_payoff_diagram(S, EX, premium, option_type):
    """
    Generates and plots the payoff diagram for an option.
    """
    s_range = np.linspace(S * 0.7, S * 1.3, 100)
    if option_type == 'call':
        payoff = np.maximum(s_range - EX, 0) - premium
    else: # put
        payoff = np.maximum(EX - s_range, 0) - premium

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(s_range, payoff, label='Profit/Loss at Expiration', color='b')
    ax.axhline(0, color='black', lw=0.5, linestyle='--')
    ax.axvline(S, color='grey', lw=0.5, linestyle='--', label=f'Current Price: ${S:.2f}')
    ax.axvline(EX, color='red', lw=0.5, linestyle='--', label=f'Strike Price: ${EX:.2f}')
    
    # Shade profit/loss regions
    ax.fill_between(s_range, payoff, where=(payoff > 0), color='green', alpha=0.2, label='Profit Zone')
    ax.fill_between(s_range, payoff, where=(payoff < 0), color='red', alpha=0.2, label='Loss Zone')

    ax.set_title(f'{option_type.capitalize()} Option Payoff Diagram', fontsize=16)
    ax.set_xlabel('Stock Price at Expiration ($)', fontsize=12)
    ax.set_ylabel('Profit / Loss ($)', fontsize=12)
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend()
    
    return fig