from ..models import Transaction
import logging
import sys
from typing import Dict, Any
import hashlib
import json
import csv
from io import StringIO
from . import coinbase, blockfi_all_transactions, blockfi_trading, cryptkeeper
from ..core.crypto_price_finder import crypto_price_finder
from datetime import datetime
from dateutil import parser

def create_import_transaction(transaction_type, asset_symbol, spot_price, datetime, asset_quantity, transaction_from, transaction_to, usd_fee, notes, user):
    """
    Generic wrapper for creating a transaction back to the database.
    If the transaction already exists, it will NOT create it, but report it as already existing.
    """
    try:
        #Splat the fields so we don't have to type them out twice
        #The hard coding of the decimals could be done better.
        transaction = {
            "transaction_type"  : transaction_type,
            "asset_symbol"      : asset_symbol,
            "spot_price"        : round(float(spot_price), 10),
            "datetime"          : parser.parse(datetime).strftime("%Y-%m-%dT%H:%M:%S"),
            "asset_quantity"    : round(float(asset_quantity), 10),
            "transaction_from"  : transaction_from,
            "transaction_to"    : transaction_to,
            "usd_fee"           : round(float(usd_fee),2) if usd_fee != "" and usd_fee != None and usd_fee != 0 else None,
            "notes"             : notes
        }
        transaction["import_hash"] = get_hash_from_dict(transaction)

        #Find the object if it exists
        exists = Transaction.objects.filter(import_hash=transaction["import_hash"], user=user)

        #Create it it if its missing, skip if it exists
        if not exists:
            Transaction.objects.create(**transaction, user=user)
            return "created"
        else:
            return "already_exists"

    except:
        logging.exception(sys.exc_info()[0])
        return "failed"

def get_hash_from_dict(dictionary: Dict[str, Any]) -> str:
    """MD5 hash of a dictionary."""
    dhash = hashlib.md5()
    # We need to sort arguments so {'a': 1, 'b': 2} is
    # the same as {'b': 2, 'a': 1}
    encoded = json.dumps(dictionary, sort_keys=True).encode()
    dhash.update(encoded)
    return dhash.hexdigest()

def get_csv_data(in_memory_file, skip_first_lines=0):
    file = in_memory_file.read().decode('utf-8')
    csv_data = csv.reader(StringIO(file), delimiter=',')

    #Custom - Skip the first line
    for x in range(skip_first_lines):
        csv_data.__next__()

    return csv_data

def get_transaction_type(type_name):

    types = {
        "Buy": Transaction.TransactionType.BUY,
        "Sell": Transaction.TransactionType.SELL,
        "Send": Transaction.TransactionType.SEND,
        "Coinbase Earn": Transaction.TransactionType.AIRDROP,
        "Rewards Income": Transaction.TransactionType.INTEREST,
    }

    if type_name in types:
        return types[type_name]

    return type_name

def process_transactions_from_file(file_name, in_memory_file, user):
    #CryptKeeper
    if cryptkeeper.file_matches_importer(file_name, in_memory_file):
        return cryptkeeper.process_transactions_from_file(in_memory_file, user)

    #Coinbase
    if coinbase.file_matches_importer(file_name, in_memory_file):
        return coinbase.process_transactions_from_file(in_memory_file, user)

    #Blockfi - Trading
    if blockfi_trading.file_matches_importer(file_name, in_memory_file):
        return blockfi_trading.process_transactions_from_file(in_memory_file, user)

    #Blockfi - All Transactions
    if blockfi_all_transactions.file_matches_importer(file_name, in_memory_file):
        return blockfi_all_transactions.process_transactions_from_file(in_memory_file, user)

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