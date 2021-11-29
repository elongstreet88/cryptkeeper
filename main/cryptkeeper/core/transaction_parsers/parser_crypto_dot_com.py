import csv
import sys
from io import StringIO
import logging
from . import tools

def file_matches_importer(file_name, in_memory_file):
    if file_name.startswith("crypto_transactions_record_"):
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
    if row[9] == "crypto_earn_interest_paid":
        return process_transactions_interest(row)

    if row[9] == "crypto_earn_program_created" or row[9] == "crypto_earn_program_withdrawn":
        #Ignored
        return []

    if row[9] == "crypto_exchange":
        return process_transactions_exchange(row)

    if row[9] == "van_purchase":
        return process_transactions_purchase(row)

    if row[9] == "crypto_deposit":
        return process_transactions_deposit(row)

    raise Exception(f"Transaction type [{row[9]}] not registered")

def process_transactions_interest(row):
    transaction = {}
    transaction["transaction_type"]     = "Interest"
    transaction["asset_symbol"]         = row[2]
    #native_amount_usd / ammount
    transaction["spot_price"]           = abs(float(row[8]) / float(row[3]))
    transaction["datetime"]             = row[0]
    transaction["asset_quantity"]       = row[3]
    transaction["transaction_from"]     = "Crypto.com"
    transaction["transaction_to"]       = "Crypto.com"
    transaction["usd_fee"]              = None
    transaction["notes"]                = f"[{row[9]}] - {row[1]}"

    return [transaction]

def process_transactions_exchange(row):
    sell_transaction = {}
    sell_transaction["transaction_type"]     = "Sell"
    #Ex: GTC -> USDC
    sell_transaction["asset_symbol"]         = row[1].split(" -> ")[0]
    #native_amount_usd / ammount
    sell_transaction["spot_price"]           = abs(float(row[8]) / float(row[3]))
    sell_transaction["datetime"]             = row[0]
    sell_transaction["asset_quantity"]       = row[3]
    sell_transaction["transaction_from"]     = "Crypto.com"
    sell_transaction["transaction_to"]       = "USD"
    sell_transaction["usd_fee"]              = None
    sell_transaction["notes"]                = f"[{row[9]}] - {row[1]}"

    buy_transaction = {}
    buy_transaction["transaction_type"]     = "Buy"
    #Ex: GTC -> USDC
    buy_transaction["asset_symbol"]         = row[1].split(" -> ")[1]
    #native_amount_usd / native_amount
    buy_transaction["spot_price"]           = abs(float(row[8]) / float(row[5]))
    buy_transaction["datetime"]             = row[0]
    buy_transaction["asset_quantity"]       = row[5]
    buy_transaction["transaction_from"]     = "USD"
    buy_transaction["transaction_to"]       = "Crypto.com"
    buy_transaction["usd_fee"]              = None
    buy_transaction["notes"]                = f"[{row[9]}] - {row[1]}"

    return [sell_transaction, buy_transaction]

def process_transactions_purchase(row):
    transaction = {}
    transaction["transaction_type"]     = "Buy"
    transaction["asset_symbol"]         = row[4]
    transaction["spot_price"]           = abs(float(row[3]) / float(row[5]))
    transaction["datetime"]             = row[0]
    transaction["asset_quantity"]       = row[5]
    transaction["transaction_from"]     = "Crypto.com"
    transaction["transaction_to"]       = "Crypto.com"
    transaction["usd_fee"]              = None
    transaction["notes"]                = f"[{row[9]}] - {row[1]}"

    return [transaction]

def process_transactions_deposit(row):
    transaction = {}
    transaction["transaction_type"]     = "Receive"
    transaction["asset_symbol"]         = row[2]
    transaction["spot_price"]           = abs(float(row[8]) / float(row[3]))
    transaction["datetime"]             = row[0]
    transaction["asset_quantity"]       = row[3]
    transaction["transaction_from"]     = "Unknown"
    transaction["transaction_to"]       = "Crypto.com"
    transaction["usd_fee"]              = None
    transaction["notes"]                = f"[{row[9]}] - {row[1]}"

    transaction["notes"]                += f". [Error] - Unable to determine sending address. Please correct manually."

    return [transaction]