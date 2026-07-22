import matplotlib.pyplot as plt

def plot_stock (data, ticker):
    # create graph
    plt.figure(figsize=(12, 6))

    # draws lines on the graph
    plt.plot(data.index, data["Close"], label="Closing Price")
    plt.plot(data.index, data["MA_5"], label="5-Day Moving Average")
    plt.plot(data.index, data["MA_20"], label="20-Day Moving Average")

    plt.title(f"{ticker} Stock Price")
    plt.xlabel("Date")
    plt.ylabel("Price ($)")

    # display graph and legend
    plt.legend()
    plt.show()