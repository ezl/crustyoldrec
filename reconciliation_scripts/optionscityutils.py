import re

# Regexes that I'll use to convert the OC name to the NE name

RE_instrument = re.compile(r'(?P<product>\w{1,3})'
                         r'-'
                         r'(?P<month>\D{3})'
                         r'(?P<year>\d{2})'
                         r' '
                         r'(?P<instrument>.*)')

RE_option = re.compile(r'(?P<strike>\d+)'
                       r'(?P<put_call>[PC])')

RE_future = re.compile(r'F')

# cleaning utility methods

def clean_price(px):
    return round(float(px) * 100, 2) / 100

def clean_trade_quantity(side, quantity):
    assert (side == "BID") or (side == "ASK")
    return (1 if side == "BID" else -1) * int(quantity)

def clean_instrument_name(description):
    return description

# helpers

OC_to_newedge_product_table = {"OZC": "CORN",
                               "ZC": "CORN"
                              }

def normalize_OC_instrument_to_newedge_format(ne_instrument):
    """Take an OC instrument name and convert it to New Edge format"""
    instrument = RE_instrument.match(ne_instrument)
    option = RE_option.match(instrument.group("instrument"))
    if option:
        """PUT FEB 11 CORN 580"""
        put_call = "PUT" if option.group("put_call") == "P" else "CALL"
        return "%s %s %s %s %s" % (put_call,
                                   instrument.group("month").upper(),
                                   instrument.group("year"),
                                   OC_to_newedge_product_table[instrument.group("product")],
                                   option.group("strike")
                                   )
    future = RE_future.match(instrument.group("instrument"))
    if future:
        """DEC 10 CORN"""
        return "%s %s %s" % (instrument.group("month").upper(),
                             instrument.group("year"),
                             OC_to_newedge_product_table[instrument.group("product")]
                             )
    raise Exception

# parse the raw mysql rows and convert to usable formats

def parse_transactions(mysql_rows):
    return [[normalize_OC_instrument_to_newedge_format( clean_instrument_name(t[2]) ),
             clean_trade_quantity(t[0], t[1]),
             clean_price(t[3])] for t in mysql_rows]

def parse_positions(mysql_rows):
    return [[normalize_OC_instrument_to_newedge_format( clean_instrument_name(t[0]) ),
             int(t[1])] for t in mysql_rows]
