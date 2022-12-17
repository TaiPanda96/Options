from Postgres.Connect import connect
from psycopg2.extras  import execute_values
import traceback

debug = False;

def bulkInsertQuery(useValues = []):
    try: 
        connection = connect()
        cursor     = connection.cursor();
        useType    = useValues[0][0] if len(useValues) > 0 else None
        useQuery   = """INSERT INTO options (
            "type",
            "contractSymbol",
            "strike",
            "currency",
            "lastPrice",
            "change",
            "percentChange",
            "volume",
            "openInterest",
            "bid",
            "ask",
            "contractSize",
            "expiration",
            "lastTradeDate",
            "impliedVolatility",
            "inTheMoney"
        ) VALUES %s
        ON CONFLICT ("contractSymbol", "expiration", "type") DO UPDATE SET 
                    type                = EXCLUDED.type,
                    "contractSymbol"    = EXCLUDED."contractSymbol",
                    strike              = EXCLUDED.strike,
                    currency            = EXCLUDED.currency,
                    "lastPrice"         = EXCLUDED."lastPrice",
                    "change"            = EXCLUDED."change",
                    "percentChange"     = EXCLUDED."percentChange",
                    volume              = EXCLUDED.volume,
                    "openInterest"      = EXCLUDED."openInterest",
                    bid                 = EXCLUDED.bid,
                    ask                 = EXCLUDED.ask,
                    "contractSize"      = EXCLUDED."contractSize",
                    expiration          = EXCLUDED.expiration,
                    "lastTradeDate"     = EXCLUDED."lastTradeDate",
                    "impliedVolatility" = EXCLUDED."impliedVolatility",
                    "inTheMoney"        = EXCLUDED."inTheMoney"
        """;
        execute_values(cursor, useQuery, useValues, template=None, page_size=100);
        debug and print("INSERT AWS options {1}: {0}".format(useType, len(useValues)))
        # commit the changes to the database
        connection.commit();
        # close communication with the database
        cursor.close();
    except Exception as e:
        traceback.print_exc()

    finally:
        if connection is not None:
            connection.close()