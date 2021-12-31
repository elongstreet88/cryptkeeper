from datetime import datetime
from crypto_price_finder import *

def test_get_usd_price():
    # Re-usables
    target_time = datetime.fromisoformat("2020-08-12T12:20:30")

    # Default
    result = get_usd_price(asset_symbol="btc")
    assert result["success"]            == True

    # Coinbase
    result = get_usd_price(asset_symbol="eth", exchange="coinbase")
    assert result["success"]            == True
    assert result["source"]             == "coinbase"

    result = get_usd_price(asset_symbol="eth", exchange="coinbase" ,target_time=target_time )
    assert result["success"]            == True
    assert result["source"]             == "coinbase"

    # Coingecko
    result = get_usd_price(asset_symbol="eth", exchange="coingecko")
    assert result["success"]            == True
    assert result["source"]             == "coingecko"

    result = get_usd_price(asset_symbol="eth", exchange="coingecko" ,target_time=target_time )
    assert result["success"]            == False