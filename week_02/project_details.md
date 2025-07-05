StatArb Alpha: Z-Score Pairs Trading with ML Prediction

Build a full pipeline to:
    1. Pull price data for stock/ETF pairs
    2. Calculate rolling spread, z-score
    3. Generate trading signal
    4. Backtest strategy performance
    5. Train an ML model to predict spread direction
    6. Evaluate & plot the ML-based signals
    7. Visualize portfolio metrics (Sharpe, Drawdown, PnL)

-----------------------------------------------------
| Concept                | Used In                  |
| ---------------------- | ------------------------ |
| Z-score, Spread        | Signal Generation        |
| Pairs Trading          | Strategy Core            |
| Sharpe Ratio, Drawdown | Evaluation               |
| ML Classification      | Predict Spread Direction |
| Lagged Features        | ML Input                 |
| Backtesting            | Strategy Validation      |
-----------------------------------------------------

🎯 Project Objectives

1. Identify Trade Opportunities:
    Use a pair of highly correlated assets (like XLK and XLF or COCA-COLA and PEPSI).
    Track how their prices diverge and converge (mean reversion idea).
2. Build Trading Logic:
    Use z-score of the price spread to generate trading signals:
    Long one, short the other when z-score is too high (expecting it to revert).
    Close when it returns to the mean.
3. Simulate Strategy Performance:
    Backtest this strategy on historical data
    Evaluate it using Sharpe ratio, drawdowns, win rate, etc.
4. Integrate Machine Learning:
    Use features like lagged z-scores, momentum, and volatility to predict the spread direction.
    Use this prediction to refine signal generation or as a standalone strategy.
5. Visualize Strategy Output:
    Build charts showing:
        Cumulative returns
        Signal overlays
        Rolling performance metrics