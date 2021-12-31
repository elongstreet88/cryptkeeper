from coingecko import *

def test_get_usd_price_current():
    result = get_usd_price_current("btc")
    assert result["asset_symbol"]       == "btc"
    assert float(result["spot_price"])  >= 0
    assert result["source"]             == "coingecko"
    assert result["success"]            == True

    result = get_usd_price_current("eth")
    assert result["asset_symbol"]       == "eth"
    assert float(result["spot_price"])  >= 0
    assert result["source"]             == "coingecko"
    assert result["success"]            == True

    result = get_usd_price_current("badcoindoesntexist1234")
    assert result["success"]            == False
    assert result["asset_symbol"]       == "badcoindoesntexist1234"
    assert result["spot_price"]         == None
    assert result["source"]             == "coingecko"
    assert len(result["message"])       >  0
    