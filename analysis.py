def print_company_info(info):

    # print info about company
    print("\nCompany Information")
    print("--------------------")
    print(f"Company: {info['longName']}")
    print(f"Sector: {info['sector']}")
    print(f"Current Price: ${info['currentPrice']:.2f}")
    print(f"Market Cap: ${(info['marketCap'] / 1_000_000_000):.2f} Billion")

    # not all companies have trailing pe and dividend yield so check first then print

    pe = info.get("trailingPE")

    if pe is not None:
        print(f"Trailing PE: {pe:.2f}")
    else:
        print("Trailing PE: N/A")

    dividend = info.get("dividendYield")

    if dividend is not None:
        print(f"Dividend Yield: {dividend * 100:.2f}%")
    else:
        print("Dividend Yield: N/A")

def print_model_performance (results):
    # print both models accuracy
    print("\nModel Performance")
    print("--------------------")
    print(f"Logistic Regression: {results['accuracy']:.2%}")
    print(f"Decision Tree: {results['tree_accuracy']:.2%}")
    print(f"Random Forest: {results['forest_accuracy']:.2%}")
    print(f"\nBest Model: {results['best_model_name']} ({results['best_accuracy']:.2%})")


def print_investment_summary (info, data, results):
    # create a score variable to keep track of stock's good points
    score = 0
    max_score = 4

    # if model predicts stock will go up tmr -> score +1
    if results["best_prediction"] == 1:
        score += 1

    # if todays price is > 20 day moving avg, increase score
    if data["Close"].iloc[-1] > data["MA_20"].iloc[-1]:
        score += 1

    # if its RSI is > 14 (its not overbought) then increase score
    if data["RSI_14"].iloc[-1] < 70 and data["RSI_14"].iloc[-1] > 30:
        score += 1

    # factor in p/e
    pe = info.get("trailingPE")

    if pe is not None and 10 <= pe <= 35:
        score += 1

    # print out investment summary
    print("\nInvestment Summary")
    print("--------------------")

    print(f"Tomorrow's Stock Movement based on Best ML Model Prediction: {'Up' if results['best_prediction'] == 1 else 'Down'}")

    # if todays closing price is greater than 20 day moving avg
    if data["Close"].iloc[-1] > data["MA_20"].iloc[-1]:
        print("20-Day Trend: Bullish")
    else:
        print("20-Day Trend: Bearish")

    # print RSI
    rsi = data["RSI_14"].iloc[-1]
    print(f"RSI: {rsi:.2f}")

    # print RSI signal
    if rsi < 30:
        print("RSI Signal: Oversold")
    elif rsi > 70:
        print("RSI Signal: Overbought")
    else:
        print("RSI Signal: Neutral")

    # display investment score and recommendation
    print(f"\nInvestment Score: {score}/{max_score}")

    if score / max_score >= .75:
        print("Recommendation: Strong Buy")
    elif score / max_score >= .50:
        print("Recommendation: Buy")
    elif score / max_score >= .25:
        print("Recommendation: Hold")
    else:
        print("Recommendation: Sell")


def print_feature_importance(results):

    # print feature importance
    print("\nRandom Forest Feature Importance")
    print("----------------------------------")

    for feature, importance in zip(results['X'].columns, results['forest_model'].feature_importances_):
        print(f"{feature}: {(importance) * 100:.2f}%")

    print("\n(Higher percentages indicate greater influence on the Random Forest's predictions)")

