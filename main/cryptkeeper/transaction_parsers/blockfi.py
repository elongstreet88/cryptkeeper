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

    #Custom - Skip the first line
    for x in range(1):
        csv_data.__next__()

    results = {
        "created"       : 0,
        "failed"        : 0,
        "already_exists": 0
    }

    for row in csv_data:
        try:
            if row[8] == "Trade":
                result = process_trade(row, user, results)
            else:
                pass
                #result = process_other(row, user)

        except:
            logging.exception(sys.exc_info()[0])
            failed +=1

    return result

def process_trade(row, user, results):
    # Process the sell portion of the swap
    try:
        transaction_type    = "Sell"
        asset_symbol        = row[7]
        spot_price           = float(row[4]) / (float(row[2]) * float(row[6])) #Sold Quantity / (Buy quant * Rate ammount)
        datetime            = row[1]
        quantity            = row[4]
        transaction_from    = "Blockfi"
        transaction_to      = "Blockfi"
        usd_transaction_fee = None
        notes               = row[0]

        result = tools.create_transaction(
            transaction_type    = transaction_type,
            asset_symbol        = asset_symbol,
            spot_price           = spot_price,
            datetime            = datetime,
            quantity            = quantity,
            transaction_from    = transaction_from,
            transaction_to      = transaction_to,
            usd_transaction_fee = usd_transaction_fee,
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
        spot_price           = row[6]
        datetime            = row[1]
        quantity            = row[2]
        transaction_from    = "Blockfi"
        transaction_to      = "Blockfi"
        usd_transaction_fee = None
        notes               = row[0]

        result = tools.create_transaction(
            transaction_type    = transaction_type,
            asset_symbol        = asset_symbol,
            spot_price           = spot_price,
            datetime            = datetime,
            quantity            = quantity,
            transaction_from    = transaction_from,
            transaction_to      = transaction_to,
            usd_transaction_fee = usd_transaction_fee,
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
    
def parse_usd_transaction_fee(data):
    if data == "" or data == "0" or data == "0.00":
        return None
    return data

def parse_transaction_from(row, transaction_type):
    if transaction_type == "Buy":
        return "USD"
    return "Coinbase"