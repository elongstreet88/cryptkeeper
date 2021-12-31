from datetime import datetime, timedelta
import requests

def get_usd_price(asset_symbol:str, target_time=None) -> dict:
    # Result Object
    result = {
        "asset_symbol"  : asset_symbol,
        "spot_price"    : None,
        "source"        : "coinbase",
        "success"       : False,
        "message"       : ""
    }

    #Move 30 seconds into the past to ensure its not a future price if target_time is provided
    if not target_time:
        target_time = datetime.utcnow() + timedelta(0, -30)

    # Coinbase pair format (ex: 'btc-usd')
    pair = f"{asset_symbol}-usd"

    # Coinbase requires start/end time fo range
    start = target_time + timedelta(0,-30) # Backwards 30 seconds
    end   = target_time + timedelta(0,30) # Forward 30 seconds

    #Cleanup Format
    start_string = start.strftime('%Y-%m-%dT%H:%M:%S')
    end_string   = end.strftime('%Y-%m-%dT%H:%M:%S')

    # Execute API call
    # Ex: https://api.exchange.coinbase.com/products/btc-usd/candles?granularity=60&start=2020-04-30%2015:15:00&end=2020-04-30%2015:16:00
    try:
        url = f"https://api.exchange.coinbase.com/products/{pair}/candles?granularity=60&start={start_string}&end={end_string}"
        headers = {"Accept": "application/json"}
        response = requests.request("GET", url, headers=headers)
        data = response.json()
    except:
        result["message"] = "Error executing API to exchange"
        return result

    if response.status_code != 200:
        result["message"] = "Error executing API to exchange"
        return result

    if len(data) == 0:
        result["message"] = "Asset not found on exchange"
        return result

    # Coinbase returns the open and close for a candle
    # For best effort calculator, we take the open and close and average it, giving the best approximation price
    # Example response:
    # [[1588259760,8827.35,8841.59,8841.59,8830.05,7.46897309],[1588259700,8841.51,8841.68,8841.51,8841.67,3.7860766]]
    price_open = float(data[0][1])
    price_close = float(data[0][2])
    spot_price = float((price_open + price_close) / 2)

    # Return
    result["success"]    = True
    result["spot_price"] = spot_price
    return result