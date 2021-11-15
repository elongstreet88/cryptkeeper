import csv
import sys
from io import StringIO
from ..models import Transaction
import logging
from . import tools
from dotmap import DotMap

def get_transactions_from_csv(in_memory_file, user):
    #CSV Reader
    file = in_memory_file.read().decode('utf-8')
    csv_data = csv.reader(StringIO(file), delimiter=',')

    #Custom - Skip the first line
    for x in range(8):
        csv_data.__next__()

    #Results object
    results = {
        "created"       : 0,
        "failed"        : 0,
        "already_exists": 0
    }

    #Iterate and process each
    for row in csv_data:
        try:
            transactions = process_transactions(row)
            for transaction in transactions:
                result = tools.create_import_transaction(**transaction, user=user)
                results[result] +=1
        except:
            logging.exception(sys.exc_info()[0])
            results["failed"] +=1

    return results

def process_transactions(row):
    #Special Cases
    if row[1] == "Convert":
        return process_transactions_convert(row)

    #Universal Parser
    transaction = {}
    transaction["transaction_type"]     = parse_transaction_type(row[1])
    transaction["asset_symbol"]         = row[2]
    transaction["spot_price"]            = row[5]
    transaction["datetime"]             = row[0]
    transaction["asset_quantity"]             = parse_asset_quantity(row[3], transaction_type = transaction["transaction_type"])
    transaction["transaction_from"]     = parse_transaction_from(row, transaction["transaction_type"])
    transaction["transaction_to"]       = parse_transaction_to(row, transaction["transaction_type"])
    transaction["usd_fee"]  = parse_usd_fee(row[8])
    transaction["notes"]                = row[9]

    return [transaction]

def process_transactions_convert(row):
    sell_transaction = {}
    sell_transaction["transaction_type"]     = "Sell"
    sell_transaction["asset_symbol"]         = row[2]
    sell_transaction["spot_price"]            = row[5]
    sell_transaction["datetime"]             = row[0]
    sell_transaction["asset_quantity"]             = float(row[3]) * -1
    sell_transaction["transaction_from"]     = "Coinbase"
    sell_transaction["transaction_to"]       = "USD"
    sell_transaction["usd_fee"]  = parse_usd_fee(row[8])
    sell_transaction["notes"]                = row[9]

    buy_transaction = {}
    buy_transaction["transaction_type"]     = "Buy"
    buy_transaction["asset_quantity"]             = float(row[9].split(" ")[-2])
    buy_transaction["asset_symbol"]         = row[9].split(" ")[-1]
    buy_transaction["spot_price"]            = float(row[5]) * float(row[3]) / buy_transaction["asset_quantity"]
    buy_transaction["datetime"]             = row[0]
    buy_transaction["transaction_from"]     = "USD"
    buy_transaction["transaction_to"]       = "Coinbase"
    buy_transaction["usd_fee"]  = None
    buy_transaction["notes"]                = row[9]

    return [sell_transaction, buy_transaction]

def parse_transaction_type(data):
    return tools.get_transaction_type(data)
    
def parse_usd_fee(data):
    if data == "" or data == "0" or data == "0.00":
        return None
    return float(data) * float(-1)

def parse_transaction_from(row, transaction_type):
    if transaction_type == "Buy":
        return "USD"
    return "Coinbase"

def parse_transaction_to(row, transaction_type):
    if (
        transaction_type == "Buy" or
        transaction_type == "Interest" or
        transaction_type == "Airdrop"
    ):
        return "Coinbase"
    if transaction_type == "Sell":
        return "USD"
    if transaction_type == "Send":
        #Parse wallet address from notes
        #Ex: '[Sent 0.09148795 ETH to 0xabcde] -> [0xabcde]'
        return row[9].split(" ")[-1]
    return "n/a"

def negative_transaction(value, transaction_type):
    if transaction_type == "Sell":
        return float(value) * float(-1)
    return value

def parse_asset_quantity(value, transaction_type):
    if transaction_type == "Sell" or transaction_type == "Send":
        return float(-1) * float(value)

    return value