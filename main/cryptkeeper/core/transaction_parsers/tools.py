import csv
from io import StringIO
from ..crypto_price_finder import crypto_price_finder
from datetime import datetime
from dateutil import parser
from . import parser_cryptkeeper, \
    parser_coinbase, \
    parser_blockfi_trading, \
    parser_blockfi_all_transactions, \
    parser_celcius, \
    parser_crypto_dot_com , \
    parser_coinbase_pro

def get_transactions_from_file(file_name, in_memory_file):
    #CryptKeeper
    if parser_cryptkeeper.file_matches_importer(file_name, in_memory_file):
        return parser_cryptkeeper.get_transactions_from_file(in_memory_file)

    #Blockfi - Trading
    if parser_blockfi_trading.file_matches_importer(file_name, in_memory_file):
        return parser_blockfi_trading.get_transactions_from_file(in_memory_file)

    #Blockfi - All Transactions
    if parser_blockfi_all_transactions.file_matches_importer(file_name, in_memory_file):
        return parser_blockfi_all_transactions.get_transactions_from_file(in_memory_file)

    #Celcius
    if parser_celcius.file_matches_importer(file_name, in_memory_file):
        return parser_celcius.get_transactions_from_file(in_memory_file)

    #Crypto.com
    if parser_crypto_dot_com.file_matches_importer(file_name, in_memory_file):
        return parser_crypto_dot_com.get_transactions_from_file(in_memory_file)

    #Coinbase
    if parser_coinbase.file_matches_importer(file_name, in_memory_file):
        return parser_coinbase.get_transactions_from_file(in_memory_file)

    #Coinbase Pro
    if parser_coinbase_pro.file_matches_importer(file_name, in_memory_file):
        return parser_coinbase_pro.get_transactions_from_file(in_memory_file)

    raise Exception(f"Unable to find valid parser for file {file_name}")

def process_missing_spot_price(transaction):
    # Get price from chain
    price_info = crypto_price_finder.get_usd_price(
        target_time     = datetime.fromisoformat(transaction["datetime"]),
        asset_symbol    = transaction["asset_symbol"]
    )
    
    if price_info["success"]:
        transaction["spot_price"] = price_info["spot_price"]
        transaction["notes"]+= " Warning - Unable to determine spot price from import automatically, best effort price added."
    else:
        transaction["needs_reviewed"] = True
        transaction["notes"]+= " Error - Unable to determine spot price from import automatically, please correct manually."

    return [transaction]