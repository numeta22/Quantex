import yfinance as yf
import requests
import json
import pandas as pd
import csv

# Get ticker input from the user
ticker = str(input("Enter the stock ticker: "))

def get_cik(ticker): 
    # Set headers
    headers = {'User-Agent': 'your@email.com'}
    url = 'https://www.sec.gov/files/company_tickers.json'


    try: 
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        for item in data.values():
            if item['ticker'] == ticker:
                return str(item['cik_str']).zfill(10)
        return "Ticker not found"
    except Exception as e:
        return f"An error fethcing CIK: {e}"

# Get ticker stock data
def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period="1y")
    return data

cik = get_cik(ticker)
print(f"CIK for {ticker}: {cik}")

df = pd.DataFrame(get_stock_data(ticker))
print(df)


