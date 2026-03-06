import os
import finnhub
from finnhub import Client
from finnhub.exceptions import FinnhubAPIException

finnhub_client = finnhub.Client(api_key="d51op5hr01qiituq5n80d51op5hr01qiituq5n8g")

# Stock candles
print(finnhub_client.stock_candles('AAPL', 'D', 1590988249, 1591852249))