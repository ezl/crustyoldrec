import MySQLdb as mysql

from datetime import date, timedelta

from optionscityutils import RE_instrument, RE_option, RE_future
from optionscityutils import (clean_trade_quantity,
                              clean_instrument_name,
                              clean_price,
                              parse_transactions,
                              parse_positions)

host = "10.51.132.92"
user = "eric"
passwd = "ziu"
db = "optionscity"

conn = mysql.connect(host=host,
                     user=user,
                     passwd=passwd,
                     db=db)

cursor = conn.cursor()

# transactions since last commit
commits_ago = 1
transactions = """SELECT TRADES_SUB.side,
                         TRADES_SUB.tradedQuantity,
                         INSTRUMENTS.displaySymbol,
                         TRADES_SUB.tradedPrice
                  FROM INSTRUMENTS,
                       TRADES,
                       TRADES_SUB
                  WHERE TRADES_SUB.tradePersistId=TRADES.persistID AND
                        TRADES.tradeDateTime > %s  AND
                        INSTRUMENTS.persistID=TRADES_SUB.instrumentPersistId
                  ORDER BY TRADES_SUB.tradePersistId;
        """ % "(SELECT commitDate FROM (SELECT commitDate FROM POSITION_COMMITS ORDER BY commitDate DESC LIMIT %s) temp ORDER BY commitDate ASC LIMIT 1)" % commits_ago

positions ="""SELECT INSTRUMENTS.displaySymbol,
                     SUM(IF(TRADES_SUB.side="BID","1","-1") * TRADES_SUB.tradedQuantity) AS qty
              FROM INSTRUMENTS,
                   INSTRUMENTMONTHS,
                   TRADES,
                   TRADES_SUB
              WHERE TRADES_SUB.tradePersistId=TRADES.persistID AND
                    INSTRUMENTS.instrumentMonth=INSTRUMENTMONTHS.persistId AND
                    TRADES.tradeDateTime > "%s" AND
                    INSTRUMENTMONTHS.expiration > (SELECT commitDate FROM POSITION_COMMITS ORDER BY commitDate DESC LIMIT 1) AND
                    INSTRUMENTS.persistID=TRADES_SUB.instrumentPersistId
              GROUP BY INSTRUMENTS.displaySymbol;
        """ % "2010-1-1 16:00:00"

cursor.execute(transactions)
rows = cursor.fetchall()
transactions = parse_transactions(rows)

cursor.execute(positions)
rows = cursor.fetchall()
positions = parse_positions(rows)
