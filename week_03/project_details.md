# StatArb Alpha: Intraday Z-Score Pairs Trading with Attribution-Aware Signals

Build a full intraday simulation to:
1. Load high-frequency price data (1-min/5-min candles)
2. Calculate dynamic hedge ratio using rolling regression
3. Compute rolling spread and z-score
4. Attribute deviation to individual assets
5. Generate precision trading signals
6. Backtest intraday execution logic
7. Visualize equity curve and trade decisions

---------------------------------------------------------
| Concept                      | Used In                  |
| --------------------------- | ------------------------ |
| Hedge Ratio (β)             | Spread Calculation        |
| Rolling Z-Score             | Signal Generation         |
| Intraday Time Series        | Realistic Trading Setup   |
| Attribution-Aware Deviation| Entry Logic Optimization  |
| Execution Simulation        | Trade Entry/Exit          |
| Position Sizing             | Capital Allocation        |
| Equity Curve, Drawdown      | Performance Evaluation    |
---------------------------------------------------------

🎯 Project Objectives

1. Use Intraday Market Data:
   Load 1-min or 5-min OHLCV candles for co-moving stock/ETF pairs like TCS-INFY or SPY-QQQ. This mimics realistic market behavior.

2. Calculate Hedge Ratio Dynamically:
   Use rolling linear regression (Y = βX + ε) to estimate hedge ratio over time.
   Compute the spread as:  

   Spread = Y - beta X

   Y=α+βX+ε
      hedge_ratio = β → tells you how many shares of X you need to hedge Y

      intercept = α → tells you the fixed offset between the two

3. Compute Z-Score of Spread:
   Normalize spread to z-score using a rolling mean and standard deviation:

   z = (soread - mu)/sigma 

   This standardization helps identify rare divergence opportunities.

4. Attribution-Aware Signal Generation:
   Instead of blindly long/shorting the spread:
   - Identify which stock deviated more from its own average.
   - Trade only the one causing divergence or size positions asymmetrically.
   - Enter trade if z-score crosses defined thresholds (e.g., ±1.0).

5. Simulate Execution Logic:
   - Enter trade on signal trigger.
   - Hold the trade while z-score reverts toward zero.
   - Exit on:
     - Mean reversion (z-score ≈ 0),
     - Profit/loss threshold,
     - Timeout (e.g., end-of-day close).

6. Position Sizing:
   Allocate capital per trade (fixed or volatility-based).
   Avoid overleveraging and simulate realistic intraday constraints.

7. Backtest and Visualize:
   - Track PnL and cumulative equity curve.
   - Analyze drawdowns, win rate, average trade return.
   - Plot signals, positions, and z-score overlays for intuition.

---

🔧 Optional Enhancements

- Rolling beta adjustment or Kalman Filter for hedge estimation.
- Add volatility-adjusted z-score thresholds.
- Add ML model (e.g., logistic regression) to predict mean reversion timing.
- Introduce stop-loss and trailing exits.
- Extend to multi-day backtests or hourly resampling.

model = sm.OLS(Y, X).fit()
This performs Ordinary Least Squares (OLS) regression:

Minimizes the sum of squared residuals:

∑_t(𝑌_t−(𝛼+𝛽𝑋_𝑡))^2
