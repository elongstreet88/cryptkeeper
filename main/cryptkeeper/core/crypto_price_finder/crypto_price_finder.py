from . import coinbase, coingecko
def get_usd_price(asset_symbol, exchange="coinbase", target_time=None) -> dict:
    """Provides a wrapper for exchange lookups. Defaults to coinbase since they support historical lookups without API key"""

    # Find the exchange provided
    match exchange:
        case "coinbase":
            return coinbase.get_usd_price(asset_symbol=asset_symbol, target_time=target_time)

        case "coingecko":
            if target_time:
                return {
                    "message" : "Coingecko does not support historical at this time",
                    "success" : False
                }
            return coingecko.get_usd_price_current(asset_symbol=asset_symbol)

        case _:
            return {
                    "message" : "Exchange not supported at this time",
                    "success" : False
                }
