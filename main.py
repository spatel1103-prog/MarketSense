import yfinance as yf

stock = yf.Ticker("AAPL")

# gets aapl stock data from past 5 years
data = stock.history(period="5y")

# create new column in data called daily_return
# daily_return represents percent change in closing price each day
data["Daily_Return"] = data["Close"].pct_change()

# create new column in data called MA_5 (5 day moving avg)
# 5 day moving avg = avg of 5 most recent closing prices
data["MA_5"] = data["Close"].rolling(window=5).mean()

# create new column in data for 20 day moving avg
data["MA_20"] = data["Close"].rolling(window=20).mean()

# create new column for moving average distance
# shows how far the current price is from its 5 day moving avg
data["MA_5_Distance"] = ( data["Close"] - data["MA_5"] ) / data["MA_5"]

# create new column for how far current price is from its 20 day moving avg
data["MA_20_Distance"] = ( data["Close"] - data["MA_20"] ) / data["MA_20"]

# create new column for momentum
# momentum = % change in closing price compared to 5 days earlier
data["Momentum_5"] = data["Close"].pct_change(periods=5)

# create new column for volatility of the stock price
# volatility measures standard dev. of daily returns over rolling 20 day period
data["Volatility_20"] = data["Daily_Return"].rolling(window=20).std()

# create new column for percent change in volume from previous day
# volume = how many shares traded during that day
data["Volume_Change"] = data["Volume"].pct_change()

# RSI - relative strength index
# momentum indicator summarizing recent gains and losses on scale of 0-100
# RSI > 70 --> overbought
# RSI < 30 --> oversold

# first calculate difference in closing price each row
price_change = data["Close"].diff()

# then separate gains and losses
gains = price_change.clip(lower = 0)
losses = -price_change.clip(upper = 0)


#data["RSI_14"] =

# prints only specified columns from data
print ( data[["Volume", "Volume_Change"]].tail(10) )
