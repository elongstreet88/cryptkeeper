from datetime import datetime, timedelta
import requests

def get_usd_price(asset_symbol, datetime):
    pair = f"{asset_symbol}-usd"

    start = datetime + timedelta(0,-30) # Backwards 30 seconds
    end   = datetime + timedelta(0,30) # Forward 30 seconds

    #Cleanup Format
    start_string = start.strftime('%Y-%m-%dT%H:%M:%S')
    end_string   = end.strftime('%Y-%m-%dT%H:%M:%S')

    #Ex: https://api.exchange.coinbase.com/products/btc-usd/candles?granularity=60&start=2020-04-30%2015:15:00&end=2020-04-30%2015:16:00
    url = f"https://api.exchange.coinbase.com/products/{pair}/candles?granularity=60&start={start_string}&end={end_string}"
    headers = {"Accept": "application/json"}
    response = requests.request("GET", url, headers=headers)
    data = response.json()

    if response.status_code != 200:
        return False, 0

    if len(data) == 0:
        return True, "Not found"

    price_open = float(data[0][1])
    price_close = float(data[0][2])

    spot_price = float((price_open + price_close) / 2)

    return True, spot_price