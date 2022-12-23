import datetime 
import requests 
import traceback 
import pytz
from   Postgres.InsertQuery import insertQuery
from   Postgres.GetQuery import getQuery
from   bs4 import BeautifulSoup
from   GetOptionsChain.Formulas import calculateEuropeanOptions
from   multiprocessing import Pool

""" Methodology: https://www.cantorsparadise.com/the-black-scholes-formula-explained-9e05b7865d8a """;
holidays =  [
        datetime.datetime(2022,1,2),
        datetime.datetime(2022,1,16),
        datetime.datetime(2022,2,20),
        datetime.datetime(2022,4,7),
        datetime.datetime(2022,5,29),
        datetime.datetime(2022,6,19),
        datetime.datetime(2022,7,3),
        datetime.datetime(2022,7,4),
        datetime.datetime(2022,9,4),
        datetime.datetime(2022,11,23),
        datetime.datetime(2022,11,24),
        datetime.datetime(2022,12,25)
    ]

headers = { 
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
        'authority': 'www.cnbc.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
        'accept': 'application/json, text/plain, */*',
        'sec-ch-ua-mobile': '?0',
    }

def getPriceQuote(symbol):
    """ This function returns the price quote for a given stock symbol. """
    url = 'https://query1.finance.yahoo.com/v7/finance/quote?symbols={}'.format(symbol)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            quoteStore = response.json();
            quote = quoteStore.get('quoteResponse', {});
            if quote is None or len(quote) == 0: return None
            useQuote = quote.get('result', []);
            if useQuote is None or len(useQuote) == 0: return None
            return {
                "symbol": useQuote[0].get('symbol', ''),
                "regularMarketPrice": useQuote[0].get('regularMarketPrice', 0.0),
            }

        else:
            return None
    except Exception as e:
        print(e)
        traceback.print_exc()


def getRiskFreeRate():
    """ This function returns the risk free rate. """
    url = 'https://www.cnbc.com/quotes/US10Y'
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser');
            priceContainer = soup.find('div', class_='QuoteStrip-lastPriceStripContainer');
            if priceContainer is None: return 
            price = priceContainer.find('span', class_='QuoteStrip-lastPrice');
            if price is not None: return float(price.text.strip().replace('%', '')) / 100;
            else: return None
        else:
            return None

    except Exception as e:
        print(e);


def getPublicylyListedHolidays():
    return {
        "numberOfTradingDays": 260 - len(holidays),
        "numberOfHolidays": len(holidays),
        "holidays": holidays
    }

def getDividendHistory(symbol):
    """ This function returns the dividend history for a given stock symbol. """
    url = 'https://api.nasdaq.com/api/quote/{}/dividends?assetclass=stocks'.format(symbol)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            quoteStore = response.json() if response else None;
            if quoteStore is None: return None;
            quote = quoteStore.get('data', None);
            if quote is None: return { "dividendDate": None, "exDividend": None}
            dividends = quote.get('dividends', {}).get('rows', [])
            if dividends is None or len(dividends) == 0: return { "dividendDate": None, "exDividend": None };
            return {
                "dividendDate": datetime.datetime.strptime(dividends[0]['exOrEffDate'], '%m/%d/%Y'),
                "exDividend": float(dividends[0]['amount'].replace('$', '')),
            }

        else:
            return None
    except Exception as e:
        print(e)
        traceback.print_exc()


def initializeInputs(symbol):
    riskFreeRate     = getRiskFreeRate();
    holidays         = getPublicylyListedHolidays();
    priceQuote       = getPriceQuote(symbol);
    dividendHistory  = getDividendHistory(symbol);
    logReturns       = getQuery("SELECT * FROM historical_returns WHERE symbol = $ ORDER BY timestamp DESC LIMIT 1",[symbol]);
    optionsContracts = getQuery("""SELECT * FROM options WHERE symbol = $ AND TO_CHAR(expiration, 'YYYY-MM-DD') >= '{}' order by expiration ASC LIMIT 300""".format((datetime.datetime.now()).strftime("%Y-%m-%d")),[symbol]);
    
    if any([riskFreeRate, holidays, priceQuote, dividendHistory, logReturns, optionsContracts]) is None: return None;
    
    return {
        "riskFreeRate": riskFreeRate,
        "tradingDays":  holidays.get('numberOfTradingDays', 252) if holidays else 252,
        "price":        priceQuote.get('regularMarketPrice', None) if priceQuote else None,
        "dividendDate": dividendHistory.get('dividendDate', None) if dividendHistory else None,
        "exDividend":   dividendHistory.get('exDividend', None) if dividendHistory else None,
        "options":      optionsContracts if len(optionsContracts) > 0 else [],
        "logReturns":   logReturns[0]['avgLogReturns'] if len(logReturns) > 0 else None,
        "standardDeviation": logReturns[0]['standardDeviation'] if len(logReturns) > 0 else None,
    }



def modelCalculator(symbol):
    computedContracts = [];
    recipeObj         = initializeInputs(symbol);
    dividend          = recipeObj.get('exDividend', None)
    riskFreeRate      = recipeObj.get('riskFreeRate', None)
    options           = recipeObj.get('options', None);
    dividendDate      = recipeObj.get('dividendDate', None)
    price             = recipeObj.get('price', None)
    tradingDays       = recipeObj.get('tradingDays',None)
    logReturns        = recipeObj.get('logReturns',None)
    standardDeviation = recipeObj.get('standardDeviation', None)

    if any([riskFreeRate, tradingDays, standardDeviation, price, dividend, dividendDate, logReturns]) is None:
        print('Missing required inputs for the model calculator:', symbol)
        return None;

    calculationObj = {
        "riskFreeRate": riskFreeRate,
        "tradingDays": tradingDays,
        "standardDeviation": standardDeviation,
        "stockPrice": price,
        "exDividend": dividend,
        "logReturns": logReturns,
        "standardDeviation": standardDeviation,
        "exDividend": dividend,
        "dividendDate": dividendDate
    };


    for contract in options:
        expirationDate   = contract['expiration'];
        recipeDate       = int(datetime.datetime(expirationDate.year, expirationDate.month, expirationDate.day, 0, 0, 0, 0).timestamp());
        # to UTC
        useExpirationDate   = pytz.utc.localize(datetime.datetime.fromtimestamp(recipeDate));
        optionPrice = calculateEuropeanOptions({** calculationObj, ** contract});
        if optionPrice is None: continue;
        priceDifference = (optionPrice / contract['lastPrice'] -1) if optionPrice is not None else None;
        obj = {
            "type": contract['type'],
            "symbol": symbol,
            "contractSymbol": contract['contractSymbol'],
            "lastPrice": float(contract.get('lastPrice', None)) if contract.get('lastPrice', None) is not None else None,
            "modelPrice": optionPrice,
            "priceDifference": priceDifference,
            "expiration": useExpirationDate,
            "impliedVolatility": contract['impliedVolatility'],
        }
        # print('Last Price', contract['lastPrice'], 'Model Price', optionPrice, 'Price Difference', priceDifference, 'Expiration', useExpirationDate, 'Implied Volatility', contract['impliedVolatility'])
        computedContracts.append(obj);

    # Insert the computed contracts into the database.
    insertQuery('priced_options',
    [
        'type',
        'symbol',
        'contractSymbol',
        'lastPrice',
        'modelPrice',
        'priceDifference',
        'expiration',
        'impliedVolatility'
    ],[tuple(i.values()) for i in computedContracts]);
    print('Completed model calculations for:', symbol);



def updateAllModelCalculatedOptions():
    tickers = ['AAPL', 'TSLA', 'AMZN', 'GOOGL', 'TSMC', 'META'];
    pool    = Pool(processes=4);
    pool.map(modelCalculator, tickers);
    pool.close();
