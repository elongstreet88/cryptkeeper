import csv
import sys
from io import StringIO
import logging
from . import tools

#
# ID	
# Time (UTC)	
# Type	
# Asset	
# Price	
# Fee	
# Quantity	
# From	
# To	
# Notes	
# Total (No Fees)	
# Total (With Fees)	
# Actions
#

def file_matches_importer(file_name, in_memory_file):
    if file_name.startswith("Cryptkeeper"):
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
        "already_exists": 0,
        "updated"       : 0,
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
    transaction = {}
    transaction["transaction_type"]     = row[2]
    transaction["asset_symbol"]         = row[3]
    transaction["spot_price"]           = float(row[4]) if row[4] != "" else ""
    #2021-09-20 12:29:14
    transaction["datetime"]             = row[1]
    transaction["asset_quantity"]       = float(row[6])
    transaction["transaction_from"]     = row[7]
    transaction["transaction_to"]       = row[8]
    transaction["usd_fee"]              = None if row[5] == "" else float(row[5])
    transaction["notes"]                = row[9]
    transaction["id"]                   = row[0]
    transaction["needs_reviewed"]       = bool(row[10])

    return [transaction]

    