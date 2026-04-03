import yfinance as yf

stock = input("Enter the stock ticker: ")
data = yf.download(stock, period='1y', interval='1d')
print(data)

# Calculate Williams %R (21-day period)
high = data['High'].rolling(21).max()
low = data['Low'].rolling(21).min()
williams_r = ((high - data['Close']) / (high - low)) * -100

print(f"Williams%R for {stock}: {williams_r}")


import requests
import pandas as pd

# Fetch company facts (balance sheet, income sattement, cash flow)
cik = '0001045810' # Example CIK for NVIDIA Corporation
url = f'https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json'
response = requests.get(url, headers={'User-Agent': 'YourApp/1.0'})
data = response.json()

# Extract assets, liabilities, equity, net income, cash flow, etc.
facts = data['facts']['us-gaap']
print(f"Assets: {facts['Assets']}")
print(f"Liabilities: {facts['Liabilities']}")
print(f"Equity: {facts['StockholdersEquity']}")

# Create a DataFrame for the financial data
# Export to a CSV

df = pd.DataFrame(data)
df.to_csv(f'data/{stock}_financial_data.csv', index=False)
