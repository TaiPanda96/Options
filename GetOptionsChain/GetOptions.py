
import requests
import traceback
import pytz
from datetime import datetime
from multiprocessing import Pool
from Postgres.InsertQuery import insertQuery

debug = False;

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    'authority': 'www.cnbc.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
    'accept': 'application/json, text/plain, */*',
    'sec-ch-ua-mobile': '?0',
}


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


def getOptionsChainByExpiration(symbol=None, expirationDate=None):
    if (symbol is None): symbol = 'AAPL';
    if (expirationDate is None): return None;
    try:
        url = 'https://query1.finance.yahoo.com/v7/finance/options/' + \
            symbol + '?date=' + str(expirationDate);
        response = requests.get(url, headers=headers).json();
        if response:
            if response.get('optionChain') is None: return
            if response.get('optionChain').get('result') is None: return
            optionsInExpirationDate = response['optionChain']['result'][0] if len(
                response['optionChain']['result']) > 0 else []
            if len(optionsInExpirationDate) == 0: return
            useOptionExpirations = optionsInExpirationDate['options'][0] if len(
                optionsInExpirationDate['options']) > 0 else []
            if len(useOptionExpirations) == 0: return
            calls = useOptionExpirations['calls'];
            puts = useOptionExpirations['puts'];
            for call in calls: {
                **call, **{'type': 'call', 'expiration': expirationDate}};
            for put in puts: {
                **put, **{'type': 'put', 'expiration': expirationDate}};

        return {
            expirationDate: {
                'calls': calls,
                'puts': puts
            }
        };
    except Exception as error:
        print(error)
        traceback.print_exc()


def getOptionsChain(symbol=None):
    if symbol is None: symbol = 'AAPL';
    try:
        url = 'https://query1.finance.yahoo.com/v7/finance/options/{}'.format(
            symbol)
        response = requests.get(url, headers=headers);
        if response.status_code == 200:
            options = response.json();
            if options is None: return
            expirationDates = options['optionChain']['result'];
            useExpirationDates = expirationDates[0]['expirationDates'] if expirationDates and len(
                expirationDates) > 0 else []
            optionsData = (getOptionsChainByExpiration(symbol, expirationDate)
                           for expirationDate in useExpirationDates);
            return {
                'symbol': symbol,
                'optionsData': list(optionsData)
            }
        else:
            return None
    except Exception as e:
        print(e)
        traceback.print_exc()


def standardizeOptionsData(optionsChain, type='call', symbol=''):
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


def updateOptionsData(symbol=None):
    if symbol is None: symbol = 'AAPL'
    updateCalls = []
    updatePuts = []
    try:
        optionsChain = getOptionsChain(symbol)
        if optionsChain is None: return None
        options = optionsChain.get(
            'optionsData', None) if optionsChain is not None else None
        if options == []: return
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
            updatePuts.append([standardizeOptionsData(i, 'put', symbol)
                               for i in puts])

        # Flatten the list of lists
        updateCalls = [tuple(item.values())
                       for sublist in updateCalls for item in sublist]
        updatePuts = [tuple(item.values())
                      for sublist in updatePuts for item in sublist]

        # Insert Calls
        if debug: print('ROWS INSERTED: {} for {} calls'.format(
            len(updateCalls), symbol))
        insertQuery('options', columns, updateCalls);

        # Insert Puts
        if debug: print('ROWS INSERTED: {} for {} puts'.format(len(updatePuts), symbol))
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