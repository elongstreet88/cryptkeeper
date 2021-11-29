import csv
import sys
from io import StringIO
import logging
from . import tools

def file_matches_importer(file_name, in_memory_file):
    if file_name.startswith("transactions-export"):
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
    if row[2] == "deposit":
        return process_transactions_deposit(row)

    if row[2] == "interest":
        return process_transactions_interest(row)

    if row[2] == "withdrawal":
        return process_transactions_withdrawal(row)

    raise Exception(f"Transaction type [{row[2]}] not registered")

def process_transactions_deposit(row):
    transaction = {}
    transaction["transaction_type"]     = "Buy"
    transaction["asset_symbol"]         = row[3]
    # usd_value/coin ammount
    transaction["spot_price"]           = float(row[5]) / float(row[4])
    transaction["datetime"]             = row[1]
    transaction["asset_quantity"]       = row[4]
    transaction["transaction_from"]     = "USD"
    transaction["transaction_to"]       = "Celcius"
    transaction["usd_fee"]              = None
    transaction["notes"]                = f"Deposit - [{row[0]}]."

    transaction["notes"]                += f" [Error] - Unable to determine if deposit transaction is 'buy' or 'recieve'. Assuming it is a 'buy'. Adjust manually if it is not."

    return [transaction]

def process_transactions_interest(row):
    transaction = {}
    transaction["transaction_type"]     = "Interest"
    transaction["asset_symbol"]         = row[3]
    # usd_value/coin ammount
    transaction["spot_price"]           = float(row[5]) / float(row[4])
    transaction["datetime"]             = row[1]
    transaction["asset_quantity"]       = row[4]
    transaction["transaction_from"]     = "Celcius"
    transaction["transaction_to"]       = "Celcius"
    transaction["usd_fee"]              = None
    transaction["notes"]                = f"Interest - [{row[0]}]."
    return [transaction]

def process_transactions_withdrawal(row):
    transaction = {}
    transaction["transaction_type"]     = "Send"
    transaction["asset_symbol"]         = row[3]
    # usd_value/coin ammount
    transaction["spot_price"]           = float(row[5]) / float(row[4])
    transaction["datetime"]             = row[1]
    transaction["asset_quantity"]       = float(row[4])
    transaction["transaction_from"]     = "Celcius"
    transaction["transaction_to"]       = "Unknown"
    transaction["usd_fee"]              = None
    transaction["notes"]                = f"Withdrawal - [{row[0]}]."

    transaction["notes"]                += f" [Error] - Unable to determine send address automatically. Please update manually."

    return [transaction]

