from data import get_company_info, get_stock_data
from indicators import calculate_indicators
from model import train_models
from analysis import (
    print_company_info,
    print_model_performance,
    print_investment_analysis,
    print_feature_importance,
)
from visualization import plot_stock


ticker = input("Enter a stock ticker: ").upper()

info = get_company_info(ticker)

data = get_stock_data(ticker)

print_company_info(info)

data = calculate_indicators(data)

results = train_models(data)

print_model_performance(results)

print_feature_importance(results)

print_investment_analysis(info, data, results)

plot_stock(data, ticker)