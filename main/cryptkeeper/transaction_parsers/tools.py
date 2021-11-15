from ..models import Transaction
import logging
import sys
from typing import Dict, Any
import hashlib
import json
import csv
from io import StringIO

def create_import_transaction(transaction_type, asset_symbol, usd_price, datetime, quantity, transaction_from, transaction_to, usd_transaction_fee, notes, user):
    """
    Generic wrapper for creating a transaction back to the database.
    If the transaction already exists, it will NOT create it, but report it as already existing.
    TODO: Add a hash field to compare in case the target has changed, aka manual overwrite, we preserve it
    """
    try:
        #Splat the fields so we don't have to type them out twice
        transaction = {
            "transaction_type"    : transaction_type,
            "asset_symbol"        : asset_symbol,
            "usd_price"           : usd_price,
            "datetime"            : datetime,
            "quantity"            : quantity,
            "transaction_from"    : transaction_from,
            "transaction_to"      : transaction_to,
            "usd_transaction_fee" : usd_transaction_fee,
            "notes"               : notes
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