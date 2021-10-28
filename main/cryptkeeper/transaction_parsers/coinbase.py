import csv
import sys
from io import StringIO
from ..models import Transaction
import logging
from . import tools

def get_transactions_from_csv(in_memory_file, user):
    #Open up CSV for read
    file = in_memory_file.read().decode('utf-8')
    csv_data = csv.reader(StringIO(file), delimiter=',')

    #Custom - Skip first 8 lines as they are garbage
    for x in range(8):
        csv_data.__next__()

    results = {
        "created"       : 0,
        "failed"        : 0,
        "already_exists": 0
    }

    for row in csv_data:
        try:
            transaction = {}
            transaction["transaction_type"]     = parse_transaction_type(row[1])
            transaction["asset_symbol"]         = row[2]
            transaction["usd_price"]            = row[5]
            transaction["datetime"]             = row[0]
            transaction["quantity"]             = row[3]
            transaction["transaction_from"]     = parse_transaction_from(row, transaction["transaction_type"])
            transaction["transaction_to"]       = parse_transaction_to(row, transaction["transaction_type"])
            transaction["usd_transaction_fee"]  = parse_usd_transaction_fee(row[8])
            transaction["notes"]                = row[9]
            transaction["user"]                 = user

            result = tools.create_import_transaction(**transaction)
            results[result] +=1

        except:
            logging.exception(sys.exc_info()[0])
            results["failed"] +=1

    return results

def parse_transaction_type(data):
    if data == "Buy":
        return "Buy"
    return data
    
def parse_usd_transaction_fee(data):
    if data == "" or data == "0" or data == "0.00":
        return None
    return data

def parse_transaction_from(row, transaction_type):
    if transaction_type == "Buy":
        return "USD"
    return "Coinbase"

def parse_transaction_to(row, transaction_type):
    if transaction_type == "Buy":
        return "Coinbase"
    if transaction_type == "Sell":
        return "USD"
    if transaction_type == "Send":
        #Parse wallet address from notes
        #Ex: 'Sent 0.09148795 ETH to 0xabcde'
        return row[9].split(" ")[-1]
    return "n/a"