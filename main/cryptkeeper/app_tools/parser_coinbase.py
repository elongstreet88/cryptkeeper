import csv
from io import StringIO
from ..models import Transaction

class row_numbers:
    transaction_type = 1

def get_transactions_from_csv(in_memory_file, user):
    file = in_memory_file.read().decode('utf-8')
    csv_data = csv.reader(StringIO(file), delimiter=',')

    #Skip first 8 lines as they are garbage
    for x in range(8):
        csv_data.__next__()

    for row in csv_data:
        print(row)
        Transaction.objects.create(
            transaction_type = parse_transaction_type(row[1]),
            asset_symbol = row[2],
            usd_price = row[5],
            datetime = row[0],
            quantity = row[3],
            transaction_from = parse_transaction_from(row),
            transaction_to = "b",
            usd_transaction_fee = parse_usd_transaction_fee(row[8]),
            user = user,
        )

def parse_transaction_type(data):
    if data == "Buy":
        return "Buy"
    return data
    
def parse_usd_transaction_fee(data):
    if data == "" or data == "0" or data == "0.00":
        return None
    return data

def parse_transaction_from(row):
    if row[1] == "Buy":
        return "USD"
    return "Coinbase"