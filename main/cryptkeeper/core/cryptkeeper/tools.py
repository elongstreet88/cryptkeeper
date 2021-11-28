import logging
import sys
from datetime import datetime
from dateutil import parser
from typing import Dict, Any
import hashlib
import json
import csv
from io import StringIO
from ...models import Transaction
from ..transaction_parsers import tools as importer_parser_tools

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

def import_transactions_from_file(file_name, in_memory_file, user):
    #Results object
    results = {
        "created"       : 0,
        "failed"        : 0,
        "already_exists": 0
    }

    valid_transactions, invalid_transactions = importer_parser_tools.get_transactions_from_file(
        file_name=file_name, 
        in_memory_file=in_memory_file
    )

    #Increment failed counter if any
    results["failed"] = len(invalid_transactions)

    #Iterate and process each
    for transaction in valid_transactions:
        try:
            result = create_import_transaction(**transaction, user=user)
            results[result] +=1
        except:
            logging.exception(sys.exc_info()[0])
            results["failed"] +=1

    return results

def get_hash_from_dict(dictionary: Dict[str, Any]) -> str:
    """MD5 hash of a dictionary."""
    dhash = hashlib.md5()
    # We need to sort arguments so {'a': 1, 'b': 2} is
    # the same as {'b': 2, 'a': 1}
    encoded = json.dumps(dictionary, sort_keys=True).encode()
    dhash.update(encoded)
    return dhash.hexdigest()