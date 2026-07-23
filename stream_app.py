import streamlit as st
from data import get_company_info, get_stock_data
from indicators import calculate_indicators
from model import train_models
from analysis import (
    print_company_info,
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
st.caption("MarketSense combines machine learning, technical indicators, and fundamental analysis to evaluate stocks.")

ticker = (st.text_input("Enter a stock ticker: ")).upper()

if st.button("Analyze"):

    st.title(f"{ticker} Analysis")

    info = get_company_info(ticker)
    data = get_stock_data(ticker)
    data = calculate_indicators(data)
    results = train_models(data)


    tab1, tab2, tab3, tab4 = st.tabs([
        "Company Information",
        "Machine Learning Models",
        "Investment Analysis",
        "Charts"
    ])

    with tab1:
        display_company_info(info)

    with tab2:
        display_model_performance(results)
        display_feature_importance(results)

    with tab3:
        display_investment_analysis(info, data, results)

    with tab4:
        fig = plot_stock(data, ticker)
        st.pyplot(fig)
