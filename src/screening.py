import requests
import json
import pandas as pd
import csv

# Fetch company facts (balance sheet, income sattement, cash flow)










cik = '0001045810' # Example CIK for NVIDIA Corporation
url = f'https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json'
response = requests.get(url, headers={'User-Agent': 'YourApp/1.0'})
data = response.json()
stock_data = json.dumps(data)
print(stock_data)


# Create a DataFrame for the financial data
# Export to a CSV

df = pd.DataFrame(data)
df.to_csv(f'data/{stock}_financial_data.csv', index=False)