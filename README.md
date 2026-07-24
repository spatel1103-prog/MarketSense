# MarketSense

MarketSense is a Python web application that analyzes stocks by combining machine learning, technical analysis, and fundamental analysis to help users evaluate potential investment opportunities. Built with Streamlit, the application provides an interactive interface where users can enter any stock ticker and instantly receive insights into the company's financial health and recent market performance.

## Screenshots
<img width="686" height="648" alt="image" src="https://github.com/user-attachments/assets/80b95a44-6df9-46f8-ac04-6f6afd37a938" />

<img width="681" height="689" alt="image" src="https://github.com/user-attachments/assets/0b90cbab-da2d-410e-9cfe-c13d3d1ff62e" />

<img width="659" height="656" alt="image" src="https://github.com/user-attachments/assets/4f80e3a0-f6f9-478b-bc70-7f99d226c473" />

<img width="682" height="685" alt="image" src="https://github.com/user-attachments/assets/2c84054f-ed4f-4c49-9a0b-78e066ab50e7" />

<img width="675" height="690" alt="image" src="https://github.com/user-attachments/assets/3ebbcb60-1460-40ae-850a-48837b615b21" />

## Features
- Analyze any publicly traded stock using its ticker symbol
- Display company information, including:
    - Current stock price
    - Market capitalization
    - P/E ratio
    - Dividend yield
- Calculate technical indicators such as:
    - 5-day Moving Average
    - 20-day Moving Average
    - Daily Returns
    - Momentum
    - Volatility
    - Volume Change
    - Relative Strength Index (RSI)
- Train and compare multiple machine learning models:
    - Logistic Regression
    - Decision Tree
    - Random Forest
- Evaluate model performance and identify the best-performing model
- Display Random Forest feature importance
- Generate an overall investment recommendation based on machine learning predictions, technical indicators, and valuation metrics
- Visualize historical stock prices alongside moving averages

## Technologies Used

- Python
- Streamlit
- Pandas
- NumPy
- yfinance
- scikit-learn
- Matplotlib

## Machine Learning

MarketSense uses historical stock data to engineer technical features and trains three supervised learning models to predict whether a stock's six-month return will be greater than or less than 10%.
After training, the application compares each model's accuracy and selects the best-performing model to contribute to the final investment analysis.

## How It Works
1. Enter a stock ticker (e.g., AAPL, MSFT, NVDA)
2. Historical stock data is downloaded using the Yahoo Finance API.
3. Technical indicators are calculated.
4. Machine learning models are trained and evaluated.
5. Company fundamentals are retrieved.
6. The application generates charts, model performance metrics, and an overall investment recommendation.
