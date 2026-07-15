# MarketSense

MarketSense is a machine learning project that analyzes historical stock market data to determine whether a stock's price will increase or decrease on the next trading day.

## Technologies
- Python
- Pandas
- NumPy
- yfinance

## Current Progress
- Historical stock data retrieval
- Feature engineering
  - Daily Return
  - Moving Averages
  - Momentum
  - Volatility
  - Volume Change
- 14 day relative strength index (RSI)
- ML target variable:
  - Tomorrow_Up (1 if the next trading day's closing price is higher than today's, otherwise 0)
