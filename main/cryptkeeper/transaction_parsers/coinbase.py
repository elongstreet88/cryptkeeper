import csv
import sys
from io import StringIO
from ..models import Transaction
import logging
from . import tools

def file_matches_importer(file_name, in_memory_file):
    if file_name.startswith("Coinbase"):
        return True
    return False

def process_transactions_from_file(in_memory_file, user):
    #Open up CSV for read
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
    if row[1] == "Buy":
        return process_transactions_buy(row)

    if row[1] == "Send":
        return process_transactions_send(row)

    if row[1] == "Coinbase Earn":
        return process_transaction_airdrop(row)

    if row[1] == "Rewards Income":
        return process_transaction_interest(row)

    if row[1] == "Convert":
        return process_transaction_convert(row)

    raise Exception(f"Transaction type [{row[8]}] not registered")

def process_transactions_buy(row):
    transaction = {}
    transaction["transaction_type"]     = "Buy"
    transaction["asset_symbol"]         = row[2]
    transaction["spot_price"]           = row[4]
    transaction["datetime"]             = row[0]
    transaction["asset_quantity"]       = row[3]
    transaction["transaction_from"]     = "USD"
    transaction["transaction_to"]       = "Coinbase"
    transaction["usd_fee"]              = float(row[7] or 0) * -1
    transaction["notes"]                = row[8]

    return [transaction]

def process_transactions_send(row):
    transaction = {}
    transaction["transaction_type"]     = "Send"
    transaction["asset_symbol"]         = row[2]
    transaction["spot_price"]           = row[4]
    transaction["datetime"]             = row[0]
    transaction["asset_quantity"]       = float(row[3]) * -1
    transaction["transaction_from"]     = "Coinbase"
    #Example: "2021-05-10T09:34:28Z	Send	ETH	0.0232917	4111.51				Sent 0.0232917 ETH to 0x60732F1Cd7d3830bBC71a6FA10CF557ce943C87f"
    transaction["transaction_to"]       = row[8].split(" ")[-1]
    transaction["usd_fee"]              = None
    transaction["notes"]                = row[8]

    #Custom Warning
    transaction["notes"]               += ". [Warning]: Unable to determine the type of send automatically. This could be a taxable event."

    return [transaction]

def process_transaction_airdrop(row):
    transaction = {}
    transaction["transaction_type"]     = "Airdrop"
    transaction["asset_symbol"]         = row[2]
    transaction["spot_price"]           = row[4]
    transaction["datetime"]             = row[0]
    transaction["asset_quantity"]       = float(row[3])
    transaction["transaction_from"]     = "Coinbase"
    transaction["transaction_to"]       = "Coinbase"
    transaction["usd_fee"]              = None
    transaction["notes"]                = row[8]

    return [transaction]

def process_transaction_interest(row):
    transaction = {}
    transaction["transaction_type"]     = "Interest"
    transaction["asset_symbol"]         = row[2]
    transaction["spot_price"]           = row[4]
    transaction["datetime"]             = row[0]
    transaction["asset_quantity"]       = float(row[3])
    transaction["transaction_from"]     = "Coinbase"
    transaction["transaction_to"]       = "Coinbase"
    transaction["usd_fee"]              = None
    transaction["notes"]                = row[8]

    return [transaction]

def process_transaction_convert(row):
    sell_transaction = {}
    sell_transaction["transaction_type"]     = "Sell"
    sell_transaction["asset_symbol"]         = row[2]
    sell_transaction["spot_price"]           = row[4]
    sell_transaction["datetime"]             = row[0]
    sell_transaction["asset_quantity"]       = float(row[3]) * -1
    sell_transaction["transaction_from"]     = "Coinbase"
    sell_transaction["transaction_to"]       = "USD"
    sell_transaction["usd_fee"]              = None
    sell_transaction["notes"]                = row[8]

    buy_transaction = {}
    buy_transaction["transaction_type"]     = "Buy"
    #Ex: Converted 5.15010367 SNX to 0.62396521 FIL
    buy_transaction["asset_quantity"]       = float(row[8].split(" ")[-2])
    buy_transaction["asset_symbol"]         = row[8].split(" ")[-1]
    # total / buy quantity = spot price
    buy_transaction["spot_price"]           = float(row[5]) / float(buy_transaction["asset_quantity"])
    buy_transaction["datetime"]             = row[0]
    buy_transaction["transaction_from"]     = "USD"
    buy_transaction["transaction_to"]       = "Coinbase"
    buy_transaction["usd_fee"]              = float(row[7]) * -1
    buy_transaction["notes"]                = row[8]

    return [sell_transaction, buy_transaction]