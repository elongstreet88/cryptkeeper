import csv
import sys
from io import StringIO
import logging
from . import tools

def file_matches_importer(file_name, in_memory_file):
    if file_name.startswith("fills"):
        return True
    return False

def get_transactions_from_file(in_memory_file):
    #Open up CSV for read
    file = in_memory_file.read().decode('utf-8')
    csv_data = csv.reader(StringIO(file), delimiter=',')

    #Custom - Skip the first line
    for x in range(1):
        csv_data.__next__()

    #Results object
    results = {
        "created"       : 0,
        "failed"        : 0,
        "already_exists": 0
    }

    #Iterate and process each
    valid_transactions = []
    invalid_transactions = []
    for row in csv_data:
        try:
            valid_transactions += process_transactions(row)
        except:
            invalid_transactions += row
            logging.exception(sys.exc_info()[0])

    return valid_transactions, invalid_transactions

def process_transactions(row):
    if row[3] == "BUY":
        return process_transactions_buy(row)

    raise Exception(f"Transaction type [{row[8]}] not registered")

def process_transactions_buy(row):
    transaction = {}
    transaction["transaction_type"]     = "Buy"
    transaction["asset_symbol"]         = row[2].split("-")[0]
    transaction["spot_price"]           = row[7]
    transaction["datetime"]             = row[4]
    transaction["asset_quantity"]       = row[5]
    transaction["transaction_from"]     = "USD"
    transaction["transaction_to"]       = "Coinbase Pro"
    transaction["usd_fee"]              = float(row[8] or 0) * -1
    transaction["notes"]                = f"{row[0]} - {row[1]} - {row[2]} - {row[3]}"

    return [transaction]