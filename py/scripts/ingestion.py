import yfinance as yf
import requests
import json
import pandas as pd

# Get ticker input from the user
ticker = str(input("Enter the stock ticker: "))

def get_cik(ticker):
    # Set headers
    headers = {'User-Agent': 'your@email.com'}
    url = 'https://www.sec.gov/files/company_tickers.json'

    tickers_cik = requests.get(url, headers=headers)

    if tickers_cik.status_code == 200:
        data = tickers_cik.json()
        ticker = ticker.upper()
        
        for item in data.values():
            if item['ticker'] == ticker:
                return str(item['cik_str']).zfill(10)
    else:

        return "Ticker not found"

# Get ticker stock data

def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period="1y")
    return data

print(get_cik(ticker))
print(get_stock_data(ticker))
