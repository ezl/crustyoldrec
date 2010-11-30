import re

#I can't extract only the columns I want when pulling the CSV, so I use transpose twice to filter it out

def transpose(x):
    return zip(*x)

def separate_headers(csv):
    csv = csv.replace('"','')
    data = [row.strip().split(",") for row in csv.strip().split("\n")]
    headers = data[0]
    rows = data [1:]
    return headers, rows

# cleaning utility methods

def clean_price(px):
    return round(float(px) * 10000, 4) / 100

def clean_trade_quantity(buy_sell_code, abs_qty):
    """Both inputs are strings from New edge.

       New edge codes: for buy=1, sell=2
       Quantity comes as a string, convert it to int
    """
    assert (buy_sell_code == "B") or (buy_sell_code == "S")
    return (1 if buy_sell_code =="B" else -1) * int(float(abs_qty))

def clean_instrument_name(description):
    return re.sub("\s{2,}"," ", description)

# parse the csv and put them into lists to match the OC lists

def parse_transactions(csv):
    headers, rows = separate_headers(csv)
    relevant_columns = ["B/S", "Quantity", "Contract Description", "Trade_price"]
    relevant_column_indices = map(lambda x: headers.index(x), relevant_columns)
    filtered = transpose([transpose(rows)[i] for i in relevant_column_indices])
    return [[clean_instrument_name(t[2]),
             clean_trade_quantity(t[0], t[1]),
             clean_price(t[3])]
            for t in filtered]

def parse_positions(csv):
    headers, rows = separate_headers(csv)
    relevant_columns = ["Contract Description", "Net Qty"]
    relevant_column_indices = map(lambda x: headers.index(x), relevant_columns)
    filtered = transpose([transpose(rows)[i] for i in relevant_column_indices])
    return [[clean_instrument_name(t[0]), int(t[1])] for t in filtered]

