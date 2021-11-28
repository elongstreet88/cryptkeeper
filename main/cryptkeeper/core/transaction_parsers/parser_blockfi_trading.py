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
    if file.startswith("Trade ID,"):
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
    if row[8] == "Trade":
        return process_transactions_trade(row)

    if row[8] == "ACH Trade":
        return process_transactions_ach_trade(row)

    raise Exception(f"Transaction type [{row[8]}] not registered")

def process_transactions_ach_trade(row):
    transaction = {}
    transaction["transaction_type"]     = "Buy"
    transaction["asset_symbol"]         = row[3].upper()
    transaction["spot_price"]           = row[6]
    transaction["datetime"]             = row[1]
    transaction["asset_quantity"]       = row[2]
    transaction["transaction_from"]     = "USD"
    transaction["transaction_to"]       = "Blockfi"
    transaction["usd_fee"]              = None
    transaction["notes"]                = "ACH Trade: " + row[0]

    return [transaction]

def process_transactions_trade(row):

    #Blockfi in all their infinite wisdom for some reason assumes the "Rate Amount" goes to the none gusd/usdc pair.
    #Its really odd, but you may see an importer have:
    #
    #trade_report.csv
    #buy currency, sold currency, rate amount
    #gusd, btc, 66000 <- This is the weird one!. It sneaks to the "sold" currency without an indicator. Very dumb
    #link, gusd, 22.32

    #To handle that, we'll set up the conditions and get it ahead of time. Thnks blockfi!
    sell_spot_price = float(0)
    buy_spot_price = float(0)

    if row[3] == "gusd" or row[3] == "usdc":
        buy_spot_price  = float(1)
        sell_spot_price = row[6]
    else:
        buy_spot_price  = row[6]
        sell_spot_price = float(row[4]) / (float(row[2]) * float(row[6])) #Sold Quantity / (Buy quant * Rate ammount)

    sell_transaction = {}
    sell_transaction["transaction_type"]     = "Sell"
    sell_transaction["asset_symbol"]         = row[5].upper()
    sell_transaction["spot_price"]           = sell_spot_price
    sell_transaction["datetime"]             = row[1]
    sell_transaction["asset_quantity"]       = float(row[4]) * -1
    sell_transaction["transaction_from"]     = "Blockfi"
    sell_transaction["transaction_to"]       = "USD"
    sell_transaction["usd_fee"]              = None
    sell_transaction["notes"]                = "Trade: " + row[0]

    buy_transaction = {}
    buy_transaction["transaction_type"]      = "Buy"
    buy_transaction["asset_symbol"]          = row[3].upper()
    buy_transaction["spot_price"]            = buy_spot_price
    buy_transaction["datetime"]              = row[1]
    buy_transaction["asset_quantity"]        = row[2]
    buy_transaction["transaction_from"]      = "USD"
    buy_transaction["transaction_to"]        = "Blockfi"
    buy_transaction["usd_fee"]               = None
    buy_transaction["notes"]                 = "Trade: " + row[0]

    return [sell_transaction, buy_transaction]

def process_trade(row, user, results):
    # Process the sell portion of the swap
    try:
        transaction_type    = "Sell"
        asset_symbol        = row[7]
        spot_price          = float(row[4]) / (float(row[2]) * float(row[6])) #Sold Quantity / (Buy quant * Rate ammount)
        datetime            = row[1]
        asset_quantity      = row[4]
        transaction_from    = "Blockfi"
        transaction_to      = "Blockfi"
        usd_fee = None
        notes               = row[0]

        result = tools.create_transaction(
            transaction_type    = transaction_type,
            asset_symbol        = asset_symbol,
            spot_price          = spot_price,
            datetime            = datetime,
            asset_quantity      = asset_quantity,
            transaction_from    = transaction_from,
            transaction_to      = transaction_to,
            usd_fee = usd_fee,
            notes               = notes,
            user                = user,
        )
        results[result] +=1
    except:
        logging.exception(sys.exc_info()[0])
        #Provide "2" failures here and go no further
        #The "sell" parse failed, we assume the "buy" would fail as well
        results["failed"] +=2
        return results

    # Process the buy portion of the swap
    try:
        transaction_type    = "Buy"
        asset_symbol        = row[3]
        spot_price          = row[6]
        datetime            = row[1]
        asset_quantity      = row[2]
        transaction_from    = "Blockfi"
        transaction_to      = "Blockfi"
        usd_fee = None
        notes               = row[0]

        result = tools.create_transaction(
            transaction_type    = transaction_type,
            asset_symbol        = asset_symbol,
            spot_price          = spot_price,
            datetime            = datetime,
            asset_quantity      = asset_quantity,
            transaction_from    = transaction_from,
            transaction_to      = transaction_to,
            usd_fee = usd_fee,
            notes               = notes,
            user                = user,
        )
        results[result] +=1
    except:
        logging.exception(sys.exc_info()[0])
        results["failed"] +=1

    return results

def process_other(row, user):
    pass

def parse_transaction_type(data):
    if data == "ACH Trade":
        return "Buy"
    return data
    
def parse_usd_fee(data):
    if data == "" or data == "0" or data == "0.00":
        return None
    return data

def parse_transaction_from(row, transaction_type):
    if transaction_type == "Buy":
        return "USD"
    return "Coinbase"