import yfinance as yf

def get_company_info (ticker):
    stock = yf.Ticker(ticker)
    return stock.info

def get_stock_data (ticker):
    stock = yf.Ticker(ticker)
    return stock.history(period="5y")