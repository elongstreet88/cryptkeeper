import pandas_datareader as web
from datetime import datetime, timedelta
import requests

def get_usd_price(datetime_string, asset_symbol):
    pair = f"{asset_symbol}-usd"

    initial = datetime.fromisoformat(datetime_string)

    start = initial + timedelta(0,-30) # Backwards 30 seconds
    end   = initial + timedelta(0,30) # Forward 30 seconds

    url = f"https://api.exchange.coinbase.com/products/{pair}/candles?granularity=60&start={start}&end={end}"
    headers = {"Accept": "application/json"}
    response = requests.request("GET", url, headers=headers)
    data = response.json()

    if len(data) == 0:
        return False, 0

    price_open = float(data[0][1])
    price_close = float(data[0][2])

    spot_price = float((price_open + price_close) / 2)

    return True, spot_price