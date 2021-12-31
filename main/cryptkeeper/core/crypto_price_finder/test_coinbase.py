from datetime import datetime
from coinbase import *

def test_get_usd_price():
    result = get_usd_price(asset_symbol="btc")
    assert result["asset_symbol"]       == "btc"
    assert float(result["spot_price"])  >= 0
    assert result["source"]             == "coinbase"
    assert result["success"]            == True

    result = get_usd_price(asset_symbol="eth")
    assert result["asset_symbol"]       == "eth"
    assert float(result["spot_price"])  >= 0
    assert result["source"]             == "coinbase"
    assert result["success"]            == True

    result = get_usd_price(asset_symbol="badcoindoesntexist1234")
    assert result["success"]            == False
    assert result["asset_symbol"]       == "badcoindoesntexist1234"
    assert result["spot_price"]         == None
    assert result["source"]             == "coinbase"
    assert len(result["message"])       >  0

    # Historical price tests
    target_time = datetime.fromisoformat("2020-08-12T12:20:30")
    result = get_usd_price(asset_symbol="btc", target_time=target_time)
    assert result["asset_symbol"]       == "btc"
    assert float(result["spot_price"])  == 11468.57
    assert result["source"]             == "coinbase"
    assert result["success"]            == True

    target_time = datetime.fromisoformat("2020-08-12T12:20:30")
    result = get_usd_price(asset_symbol="eth", target_time=target_time)
    assert result["asset_symbol"]       == "eth"
    assert float(result["spot_price"])  == 381.525
    assert result["source"]             == "coinbase"
    assert result["success"]            == True