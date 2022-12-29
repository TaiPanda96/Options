
import requests
import traceback
import pytz
from   datetime import datetime
from   multiprocessing import Pool
from   Postgres.InsertQuery import insertQuery

columns = [
    'type',
    'symbol',
    'contractSymbol',
    'strike',
    'currency',
    'lastPrice',
    'change',
    'percentChange',
    'volume',
    'openInterest',
    'bid',
    'ask',
    'contractSize',
    'expiration',
    'lastTradeDate',
    'impliedVolatility',
    'inTheMoney'
];

def getOptionsChain(symbol='AAPL'):
    try:
        url = 'https://kf1wexbj85.execute-api.us-east-2.amazonaws.com/Prod/get-options?ticker={}'.format(
            symbol)
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        print(e)
        traceback.print_exc(exec_info=True)


def standardizeOptionsData(optionsChain, type='call', symbol = ''):
    optionsData = {
        "type": type,
        "symbol": symbol,
        "contractSymbol": optionsChain.get('contractSymbol', ''),
        "strike": optionsChain.get('strike', 0.0),
        "currency": optionsChain.get('currency', "USD"),
        "lastPrice": optionsChain.get('lastPrice', 0.0),
        "change": optionsChain.get('change', 0.0),
        "percentChange": optionsChain.get('percentChange', 0.0),
        "volume": optionsChain.get('volume', 0),
        "openInterest": optionsChain.get('openInterest', 0),
        "bid": optionsChain.get('bid', 0.0),
        "ask": optionsChain.get('ask', 0.0),
        "contractSize": optionsChain.get('contractSize', None),
        "expiration": optionsChain.get('expiration', None),
        "lastTradeDate": optionsChain.get('lastTradeDate', 0),
        "impliedVolatility": optionsChain.get('impliedVolatility', 0.0),
        "inTheMoney": 'false' if optionsChain.get('inTheMoney', 'false') == False else 'true'
    }
    if optionsData['expiration'] is not None:
        optionsData['expiration'] = pytz.utc.localize(
            datetime.fromtimestamp(optionsData['expiration']))
    if optionsData['lastTradeDate'] is not None:
        optionsData['lastTradeDate'] = pytz.utc.localize(
            datetime.fromtimestamp(optionsData['lastTradeDate']))

    return optionsData

def updateOptionsData(symbol = 'TSLA'):
    updateCalls = []
    updatePuts  = []
    try:
        optionsChain = getOptionsChain(symbol)
        if optionsChain is None: return None
        options = optionsChain.get('optionsData', None) if optionsChain is not None else None
        dates = [i.keys() for i in options]
        # Flatten the list of lists
        dates = [item for sublist in dates for item in sublist]

        for i in options:
            expirationDates = i.keys() if i is not None else None
            if expirationDates is None:
                continue
            date = list(expirationDates)[
                0] if expirationDates is not None else None
            optionContract = i.get(date, None) if i is not None else None
            if optionContract is None:
                continue

            # Get Calls
            calls = optionContract.get(
                'calls', None) if optionContract is not None else None
            puts = optionContract.get(
                'puts', None) if optionContract is not None else None

            updateCalls.append([standardizeOptionsData(i, 'call', symbol)
                               for i in calls])
            updatePuts.append([standardizeOptionsData(i, 'put',symbol) 
                               for i in puts])

        # Flatten the list of lists
        updateCalls = [tuple(item.values())
                       for sublist in updateCalls for item in sublist]
        updatePuts  = [tuple(item.values())
                      for sublist in updatePuts for item in sublist]

        # Insert Calls
        insertQuery('options',columns,updateCalls);

        # Insert Puts
        insertQuery('options',columns,updatePuts);

    except Exception as e:
        print(e)
        traceback.print_exc()

    finally:
        print('Update completed for {} options at {}'.format(symbol, datetime.now()))


def updateAllOptions():
    tickers = ['AAPL', 'TSLA', 'AMZN', 'GOOGL', 'TSMC', 'META'];
    pool    = Pool(processes=6);
    pool.map(updateOptionsData, tickers);
    pool.close();