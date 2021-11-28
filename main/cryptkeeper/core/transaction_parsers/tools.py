import logging
import sys
from typing import Dict, Any
import hashlib
import json
import csv
from io import StringIO
from . import parser_cryptkeeper, parser_coinbase, parser_blockfi_trading, parser_blockfi_all_transactions
from ..crypto_price_finder import crypto_price_finder
from datetime import datetime
from dateutil import parser

def get_csv_data(in_memory_file, skip_first_lines=0):
    file = in_memory_file.read().decode('utf-8')
    csv_data = csv.reader(StringIO(file), delimiter=',')

    #Custom - Skip the first line
    for x in range(skip_first_lines):
        csv_data.__next__()

    return csv_data

def get_transactions_from_file(file_name, in_memory_file):
    #CryptKeeper
    if parser_cryptkeeper.file_matches_importer(file_name, in_memory_file):
        return parser_cryptkeeper.get_transactions_from_file(in_memory_file)

    #Coinbase
    if parser_coinbase.file_matches_importer(file_name, in_memory_file):
        return parser_coinbase.get_transactions_from_file(in_memory_file)

    #Blockfi - Trading
    if parser_blockfi_trading.file_matches_importer(file_name, in_memory_file):
        return parser_blockfi_trading.get_transactions_from_file(in_memory_file)

    #Blockfi - All Transactions
    if parser_blockfi_all_transactions.file_matches_importer(file_name, in_memory_file):
        return parser_blockfi_all_transactions.get_transactions_from_file(in_memory_file)

def process_missing_spot_price(transaction):
    # Get price from chain
    success, spot_price = crypto_price_finder.get_usd_price(
        datetime        = datetime.fromisoformat(transaction["datetime"]),
        asset_symbol    = transaction["asset_symbol"]
    )
    if success:
        transaction["spot_price"] = spot_price
        transaction["notes"]+= " Warning - Unable to determine spot price from import automatically, best effort price added."
        return [transaction]

    transaction["notes"]+= " Error - Unable to determine spot price from import automatically, please correct manually."

    return [transaction]