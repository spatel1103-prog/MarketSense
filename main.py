import yfinance as yf
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier

ticker = input("Enter a stock ticker: ").upper()
stock = yf.Ticker(ticker)

# stock.info is a python dictionary that gives info abt the company
info = stock.info

# print info about comapny
print("\nCompany Information")
print("--------------------")
print(f"Company: {info['longName']}")
print(f"Sector: {info['sector']}")
print(f"Current Price: ${info['currentPrice']: .2f}")
print(f"Market Cap: ${(info['marketCap'] / 1_000_000_000):.2f} Billion")
print(f"Trailing PE: {info['trailingPE']}")
print(f"Dividend Yield: {info['dividendYield']}%")


# gets stock data from past 5 years
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

# we have to average the gains and losses
# relative strength = avg gain / avg loss
avg_gains = gains.rolling(window=14).mean()
avg_losses = losses.rolling(window=14).mean()
rs = avg_gains / avg_losses

# use RSI formula to calculate
# if avg gains are much larger than avg losses then rsi is closer to 100 and vice versa
# we are looking at a 14 day rolling window so its RSI_14
data["RSI_14"] = 100 - (100 / (1 + rs))

# make a column that has the next days closing price using shift
data["Close_Shifted"] = data["Close"].shift(-1)

# create column named tomorrow_up that displays 1 if it goes up the next day and 0 if it goes down
data["Tomorrow_Up"] = (data["Close_Shifted"] > data["Close"]).astype(int)

# remove rows with NaN
clean_data = data.dropna()

# X = info we give the model to use (columns we have created)
# y = what we're trying to predict (tomorrow up)

X = clean_data[[
        "Daily_Return", "MA_5_Distance",
        "MA_20_Distance", "Momentum_5",
        "Volatility_20", "Volume_Change", "RSI_14"
    ]]

y = clean_data["Tomorrow_Up"]

# train on 80% of the data and test on 20%
# dont shuffle data because this data is chronological
X_train, X_test, y_train, y_test = train_test_split ( X, y, test_size=0.2, shuffle=False)

# create logistic regression model object
model = LogisticRegression()

# model looks at training examples and tries to learn patterns between X and y
model.fit( X_train, y_train )

# predictions is a NumPy array now not a dataframe
predictions = model.predict(X_test)

# print predictions the model made
# :10 because we slice it like a python list
print ( f"\n{predictions[:10]}" )

## see what actual results were
print ( y_test.head(10) )

## calculates accuracy of model using its results and the real results
accuracy = accuracy_score (y_test, predictions)

# now use decision tree model to compare against logistics regression model
# set random state to 42 so that it builds the random tree the same way every time u run
tree_model = DecisionTreeClassifier(random_state=42)

tree_model.fit(X_train, y_train)
tree_predictions = tree_model.predict(X_test)
tree_accuracy = accuracy_score (y_test, tree_predictions)

# print both models accuracy
print("\nModel Performance")
print("--------------------")
print(f"Logistic Regression: {accuracy:.2%}")
print(f"Decision Tree: {tree_accuracy:.2%}")

# create graph
plt.figure ( figsize =(12,6) )

# draws lines on the graph
plt.plot(data.index, data["Close"], label="Closing Price")
plt.plot( data.index, data["MA_5"], label="5-Day Moving Average")
plt.plot( data.index, data["MA_20"], label="20-Day Moving Average")

plt.title(f"{ticker} Stock Price")
plt.xlabel("Date")
plt.ylabel("Price ($)")

# display graph and legend
plt.legend()
plt.show()

# create a score variable to keep track of stock's good points
score = 0

# if model predicts stock will go up tmr -> score +1
if predictions[-1] == 1:
    score += 1

# if todays price is > 20 day moving avg, increase score
if data["Close"].iloc[-1] > data["MA_20"].iloc[-1]:
    score += 1

# if its RSI is > 14 (its not overbought) then increase score
if data["RSI_14"].iloc[-1] < 70:
    score += 1


# print out investment summary
print("\nInvestment Summary")
print("--------------------")

print(f"Tomorrow's Stock Movement based on Machine Learning Prediction: {'Up' if predictions[-1] == 1 else 'Down'}")

# if todays closing price is greater than 20 day moving avg
if data["Close"].iloc[-1] > data["MA_20"].iloc[-1]:
    print("20-Day Trend: Bullish")
else:
    print("20-Day Trend: Bearish")

rsi = data["RSI_14"].iloc[-1]
print(f"RSI: {rsi:.2f}")

if rsi < 30:
    print("RSI Signal: Oversold")
elif rsi > 70:
    print("RSI Signal: Overbought")
else:
    print("RSI Signal: Neutral")

print(f"\nInvestment Score: {score}/3")

if score == 3:
    print("Recommendation: Strong Buy")
elif score == 2:
    print("Recommendation: Buy")
elif score == 1:
    print("Recommendation: Hold")
else:
    print("Recommendation: Sell")