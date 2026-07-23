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
        print(f"Dividend Yield: {dividend:.2f}%")
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

    # if model predicts stock will go up 10% in next 6 months -> score +1
    if results['best_accuracy'] >= 0.60 and results["best_prediction"] == 1:
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

    if ( results['best_accuracy'] >= .60 ):
        print(f"Predicted 6 Month Return with {(results['best_accuracy'] * 100):.2f}% accuracy: {'> 10%' if results['best_prediction'] == 1 else '< 10%'}")
    else:
        print("Model accuracy too low to make a reliable prediction about future 6-month return")

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



def print_investment_analysis (info, data, results):

    # keep track of score through each section
    score = 0
    max_score = 10

    print("\nInvestment Analysis")
    print("======================")

    print("\nMachine Learning")
    print("-------------------")

    # display model results and accuracy
    if results['best_prediction'] == 1:
        print("Predicted 6-Month Return: > 10%")
    else :
        print("Predicted 6-Month Return: < 10%")

    print(f"Model Accuracy: {(results['best_accuracy']) * 100:.2f}%")

    # if model accuracy is low, dont include in score
    if results['best_accuracy'] < 0.6:
        print("** Not included in overall score due to low confidence **")
        max_score -= 2

    # if model accuracy is good and 6-month return is predicted to be > 10%, score +2
    if results['best_accuracy'] >= 0.60 and results['best_prediction'] == 1:
        score += 2
        print("ML Score: Positive (+2)")
    elif results['best_accuracy'] >= 0.60 and results['best_prediction'] == 0:
        print("ML Score: Negative (+0)")


    print("\nTechnical Analysis")
    print("---------------------")

    # if todays price is > 20 day moving avg, increase score
    if data["Close"].iloc[-1] > data["MA_20"].iloc[-1]:
        score += 1
        print("20-Day Trend: Bullish (+1)")
    else :
        print("20-Day Trend: Bearish")

    print(f"Current Price: ${data['Close'].iloc[-1]:.2f}")
    print(f"20-Day Moving Avg: ${data['MA_20'].iloc[-1]:.2f}\n")


    # if its RSI is between 30 and 70 --> increase score
    if data["RSI_14"].iloc[-1] < 70 and data["RSI_14"].iloc[-1] > 30:
        score += 1
        print(f"RSI: {data['RSI_14'].iloc[-1]:.2f} (Healthy) (+1)\n")
    elif data["RSI_14"].iloc[-1] > 70:
        print(f"RSI: {data['RSI_14'].iloc[-1]:.2f} (Overbought)\n")
    elif data["RSI_14"].iloc[-1] < 30:
        print(f"RSI: {data['RSI_14'].iloc[-1]:.2f} (Oversold)\n")

    # check if momentum is positive or negative
    if data['Momentum_5'].iloc[-1] > 0:
        score += 1
        print("Momentum: Positive (+1)\n")
    else :
        print("Momentum: Negative\n")

    # check volatility, low volatility is better so increase score
    if data['Volatility_20'].iloc[-1] < .02:
        score += 1
        print(f"20-Day Volatility: {data['Volatility_20'].iloc[-1]:.2%} (Low) (+1)")
    elif data['Volatility_20'].iloc[-1] > .02 and data['Volatility_20'].iloc[-1] < .04:
        print(f"20-Day Volatility: {data['Volatility_20'].iloc[-1]:.2%} (Moderate)")
    elif data['Volatility_20'].iloc[-1] > .04:
        print(f"20-Day Volatility: {data['Volatility_20'].iloc[-1]:.2%} (High)")


    print("\nFundamental Analysis")
    print("----------------------")

    # evaluate companys revenue growth
    revenue = info.get("revenueGrowth")
    if revenue is None:
        print("Revenue Growth: N/A")
    elif revenue > 0:
        score += 1
        print(f"Revenue Growth: {revenue:.1%} (+1)")
    else:
        print(f"Revenue Growth: {revenue:.1%}")

    # evaluate profit margin
    # higher profit margin indicate stronger business
    margin = info.get("profitMargins")
    if margin is None:
        print("Profit Margin: N/A")
    elif margin >= 0.10:
        score += 1
        print(f"Profit Margin: {margin:.1%} (+1)")
    else:
        print(f"Profit Margin: {margin:.1%}")

    # evaluate return on equity
    # ROE = how efficiently do they generate profit from shareholders money
    roe = info.get("returnOnEquity")
    if roe is None:
        print("Return on Equity: N/A")
    elif roe >= 0.15:
        # generally ROE > 15% is considered good
        score += 1
        print(f"Return on Equity: {roe:.1%} (+1)")
    else:
        print(f"Return on Equity: {roe:.1%}")

    # moderate pe is good so if pe is in range then increase score
    pe = info.get("trailingPE")
    if pe is None:
        print("Trailing PE: N/A")
    elif 10 <= pe <= 35:
        score += 1
        print(f"Trailing PE: {pe:.2f} (Fairly Valued) (+1)")
    else:
        print(f"Trailing PE: {pe:.2f} (Outside Preferred Range)")


    print("\nOverall Analysis")
    print("----------------")

    overall_score = score / max_score
    print(f"Overall Score: {score}/{max_score}  ({overall_score * 100:.2f}%)")

    if overall_score >= 0.85:
        recommendation = "Strong Buy"
    elif overall_score >= 0.70:
        recommendation = "Buy"
    elif overall_score >= 0.50:
        recommendation = "Hold"
    else:
        recommendation = "Sell"

    print(f"Recommendation: {recommendation} ")



def print_feature_importance(results):

    print("\nRandom Forest Feature Importance")
    print("----------------------------------")

    for feature, importance in zip(results['X'].columns, results['forest_model'].feature_importances_):
        print(f"{feature}: {(importance) * 100:.2f}%")

    print("\n(Higher percentages indicate greater influence on the Random Forest's predictions)")

