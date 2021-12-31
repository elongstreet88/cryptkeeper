from pycoingecko import CoinGeckoAPI

def get_usd_price_current(asset_symbol:str) -> dict:
    # Get API
    cg = CoinGeckoAPI()

    # Result Object
    result = {
        "asset_symbol"  : asset_symbol,
        "spot_price"    : None,
        "source"        : "coingecko",
        "success"       : False,
        "message"       : ""
    }

    # Coingecko only supports asset names (ex: bitcoin) vs the symbol (ex: btc)
    # Anoyingly, that means we have to do a lookup
    # They DO publish a full list that can be looked up from however
    #
    # This creates a dict of:
    # {
    #    "btc" : "bitcoin",
    #    "eth" : "ethereum",
    #    ...
    # }
    # We'll use this to do the correct lookups
    coin_list               = cg.get_coins_list()
    symbol_to_name_lookup   = {}

    for coin in coin_list:
        symbol_to_name_lookup[coin['symbol']] = coin['id']

    # If it doesn't have the key, exchange doesn't have it, so error out
    if asset_symbol.lower() not in symbol_to_name_lookup:
        result["message"] = "Exchange does not have this symbol listed, no spot price returned"
        return result
    
    # We now have the asset name (ex: bitcoin)
    asset_name = symbol_to_name_lookup[asset_symbol.lower()]

    # Execute the price api call
    # {'bitcoin': {'usd': 48976}} -> {'usd': 48976}
    try:
        response = cg.get_price(ids=asset_name, vs_currencies='usd')[asset_name]
    except:
        result["message"] = "Error executing API to exchange"
        return result

    # Set price and return
    result["spot_price"] = response["usd"]
    result["success"]    = True
    return result