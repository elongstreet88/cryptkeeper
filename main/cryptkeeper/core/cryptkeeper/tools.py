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

def create_import_transaction(transaction_type, asset_symbol, spot_price, datetime, asset_quantity, transaction_from, transaction_to, usd_fee, notes, user, id=None):
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

        existing_id, hash_matches = find_existing_import_transaction(
            user        = user,
            import_hash = transaction["import_hash"], 
            id          = id
        )

        # A matching hash means no updates, return
        if hash_matches:
            return "already_exists"

        if existing_id:
            #If id was determined, update
            obj = Transaction.objects.filter(pk=existing_id)
            obj.update(**transaction)
            return "updated"
        else:
            #If id not determined, create
            Transaction.objects.create(**transaction, user=user)
            return "created"

    except:
        logging.exception(sys.exc_info()[0])
        return "failed"

def find_existing_import_transaction(user, import_hash, id=None):
    """
    Finds an existing transaction based on [import_hash] and [id].
    It will try both and return the id if found and hash_matches = True if hash matches
    """
    #Try to match on Id if provided
    if id:
        obj = Transaction.objects.filter(pk=id, user=user)

        # Matched id successfully, hash matches
        if obj and obj[0].import_hash == import_hash:
            return id, True
        
        # Matched id successfully, hash doesn't match
        if obj:
            return id, False

    #Try to match on import_hash alone
    if not id:
        obj = Transaction.objects.filter(import_hash=import_hash, user=user)

        # Matched id successfully, hash matches
        if obj and obj[0].import_hash == import_hash:
            return id, True

        #matched id successfully
        if obj:
            return id, False

    # Did not match any
    return None, False

def import_transactions_from_file(file_name, in_memory_file, user):
    #Results object
    results = {
        "created"       : 0,
        "failed"        : 0,
        "already_exists": 0,
        "updated"       : 0,
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