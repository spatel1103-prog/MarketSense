import streamlit as st
from data import get_company_info, get_stock_data
from indicators import calculate_indicators
from model import train_models
from analysis import (
    print_company_info,
    display_company_info,
    print_model_performance,
    display_model_performance,
    print_investment_analysis,
    print_feature_importance,
    display_feature_importance,
    display_company_info,
    display_investment_analysis
)
from visualization import plot_stock



st.title("MarketSense")

ticker = st.text_input("Enter a stock ticker: ")

if st.button("Analyze"):
    info = get_company_info(ticker)

    data = get_stock_data(ticker)


    display_company_info(info)

    data = calculate_indicators(data)

    results = train_models(data)

    display_model_performance(results)

    display_feature_importance(results)

    display_investment_analysis(info, data, results)

    # plot_stock(data, ticker)