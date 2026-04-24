from edgar import *
import pandas as pd
import csv

set_identity("your.name@example.com")

# --- Get financial statements ---

tickers = ["IONQ", "NVDA", "AAPL", "MSFT", "GOOG"]

rows = []
for ticker in tickers:
    metrics = Company(ticker).get_financials().get_financial_metrics()
    metrics["ticker"] = ticker
    rows.append(metrics)

df = pd.DataFrame(rows)
print(df)

# --- Export to CSV ---
financials = df.to_csv("financials.csv", index=False)