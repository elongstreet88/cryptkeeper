import csv
import sys
from io import StringIO
import logging
from . import tools

def file_matches_importer(file_name, in_memory_file):
    if not file_name.startswith("trade_report_all"):
        return False

    file = in_memory_file.read().decode('utf-8')
    in_memory_file.seek(0) #Always reset
    if file.startswith("Cryptocurrency,"):
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
    #Special Cases
    if row[2] == "Trade" or row[2] == "Ach Trade":
        return [] #Skip. These are covered by "trade" report already more accurately

    if row[2] == "Ach Deposit":
        return process_transaction_ach_deposit(row)

    if row[2] == "Bonus Payment" or row[2] == "Referral Bonus":
        return process_transaction_bonus(row)

    if row[2] == "Deposit":
        return process_transaction_deposit(row)

    if row[2] == "Interest Payment":
        return process_transaction_interest_payment(row)

    if row[2] == "Withdrawal":
        return process_transaction_interest_withdrawal(row)

    raise Exception(f"Transaction type [{row[8]}] not registered")

def process_transaction_ach_deposit(row):
    transaction = {}
    transaction["transaction_type"]     = "Buy"
    transaction["asset_symbol"]         = row[0]
    transaction["spot_price"]           = float(1) #Always buy GUSD AT $1
    transaction["datetime"]             = row[3]
    transaction["asset_quantity"]       = float(row[1])
    transaction["transaction_from"]     = "USD"
    transaction["transaction_to"]       = "Blockfi"
    transaction["usd_fee"]              = None
    transaction["notes"]                = f"Ach Deposit: {row[1]} {row[0]}"

    return [transaction]

def process_transaction_bonus(row):
    transaction = {}
    transaction["transaction_type"]     = "Airdrop"
    transaction["asset_symbol"]         = row[0]
    transaction["datetime"]             = row[3]
    transaction["asset_quantity"]       = float(row[1])
    transaction["transaction_from"]     = "Blockfi"
    transaction["transaction_to"]       = "Blockfi"
    transaction["usd_fee"]              = None
    transaction["notes"]                = f"Bonus: {row[1]} {row[0]}."

    if row[0] == "GUSD" or row[0] == "USDC":
        #Blockfi spot price always 1 for stables
        transaction["spot_price"] = float(1)
        return [transaction]

    # Get price from chain if possible
    tools.process_missing_spot_price(transaction)

    return [transaction]

def process_transaction_deposit(row):
    transaction = {}
    transaction["transaction_type"]     = "Receive"
    transaction["asset_symbol"]         = row[0]
    transaction["spot_price"]           = float(1) if row[0] == "GUSD" else float("0")
    transaction["datetime"]             = row[3]
    transaction["asset_quantity"]       = float(row[1])
    transaction["transaction_from"]     = "Unknown"
    transaction["transaction_to"]       = "Blockfi"
    transaction["usd_fee"]              = None
    transaction["notes"]                = f"Deposit: {row[1]} {row[0]}."
    #custum for deposit
    transaction["notes"]                += " Unable to determine [from] field from transaction report. Please correct manually."

    if row[0] == "GUSD" or row[0] == "USDC":
        #Blockfi spot price always 1 for stables
        transaction["spot_price"] = float(1)
        return [transaction]

    # Get price from chain if possible
    tools.process_missing_spot_price(transaction)

    return [transaction]

def process_transaction_interest_payment(row):
    transaction = {}
    transaction["transaction_type"]     = "Interest"
    transaction["asset_symbol"]         = row[0]
    #transaction["spot_price"]          = float(1) if row[0] == "GUSD" or row[0] == "USDC" else float("0")
    transaction["datetime"]             = row[3]
    transaction["asset_quantity"]       = float(row[1])
    transaction["transaction_from"]     = "Blockfi"
    transaction["transaction_to"]       = "Blockfi"
    transaction["usd_fee"]              = None
    transaction["notes"]                = f"Interest Payment: {row[1]} {row[0]}."

    if row[0] == "GUSD" or row[0] == "USDC":
        #Blockfi spot price always 1 for stables
        transaction["spot_price"] = float(1)
        return [transaction]

    # Get price from chain if possible
    tools.process_missing_spot_price(transaction)

    return [transaction]

def process_transaction_interest_withdrawal(row):
    transaction = {}
    transaction["transaction_type"]     = "Send"
    transaction["asset_symbol"]         = row[0]
    transaction["spot_price"]           = float(1) if row[0] == "GUSD" or row[0] == "USDC" else float("0")
    transaction["datetime"]             = row[3]
    transaction["asset_quantity"]       = float(row[1])
    transaction["transaction_from"]     = "Blockfi"
    transaction["transaction_to"]       = "Unknown"
    transaction["usd_fee"]              = None
    transaction["notes"]                = f"Withdrawal: {row[1]} {row[0]}."
    # Custom for withdrawl
    transaction["notes"]                += " Error - Unable to determine [to] field from transaction report, please correct manually."

    if row[0] == "GUSD" or row[0] == "USDC":
        #Blockfi spot price always 1 for stables
        transaction["spot_price"] = float(1)
        return [transaction]

    # Get price from chain if possible
    tools.process_missing_spot_price(transaction)

    return [transaction]