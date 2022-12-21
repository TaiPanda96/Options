import datetime 
import requests 
import traceback 
import pprint
import math 
import pytz
from   bs4 import BeautifulSoup
from   Postgres.InsertQuery import insertQuery
from   Postgres.GetQuery import getQuery
from   datetime import timedelta
from   GetOptionsChain.Formulas import laplaceDistributionCDF

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
            quoteStore = response.json() if response else None;
            if quoteStore is None: return None;
            quote = quoteStore.get('quoteResponse', {}).get('result', [])[0];
            return {
                "symbol": quote.get('symbol', ''),
                "regularMarketPrice": quote.get('regularMarketPrice', 0.0),
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
            quote = quoteStore.get('data', {});
            dividends = quote['dividends']['rows'];
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
    optionsContracts = getQuery("""SELECT * FROM options WHERE symbol = $ order by expiration DESC""",[symbol]);
    return {
        "riskFreeRate": riskFreeRate,
        "tradingDays": holidays['numberOfTradingDays'],
        "price": priceQuote['regularMarketPrice'],
        "dividendDate": dividendHistory['dividendDate'],
        "exDividend": dividendHistory['exDividend'],
        "options": optionsContracts,
        "logReturns": logReturns[0]['avgLogReturns'],
        "standardDeviation": logReturns[0]['standardDeviation'],
    }

def calculateAmericanOptions(optionsContracts, distributionType = 'la place'):
    return 


def calculateEuropeanOptions(optionsContracts, distributionType = 'la place'):
    return


def modelCalculator(symbol):
    recipeObj         = initializeInputs(symbol);
    dividend          = recipeObj['exDividend'];
    riskFreeRate      = recipeObj['riskFreeRate'];
    options           = recipeObj['options'];
    dividendDate      = recipeObj['dividendDate'];
    price             = recipeObj['price'];
    tradingDays       = recipeObj['tradingDays'];
    logReturns        = recipeObj['logReturns'];
    standardDeviation = recipeObj['standardDeviation'];

    optimalToExcerciseEarly   = [];
    notOptimalToExerciseEarly = [];

    optionsToCalculate = {};
    # Evaluate Dividends Inequality to Determine Point in Time or Continous Exercise
    if dividendDate is not None and dividend is not None:
        # American Options
        for contract in options:
            strike           = contract['strike'];
            expirationDate   = contract['expiration'];

            timediff = expirationDate - pytz.utc.localize(dividendDate)
            days     = timediff.days;

            if dividend <= strike * ( 1 - math.exp(riskFreeRate * -1 * (days))): optimalToExcerciseEarly.append(contract);
            else: notOptimalToExerciseEarly.append(contract);

        optionsToCalculate['excerciseEarly']    = optimalToExcerciseEarly;
        optionsToCalculate['notExcerciseEarly'] = notOptimalToExerciseEarly;

        # Calculate American Options

    # European Options
    else: optionsToCalculate['options'] = options;

    pprint.pprint(optionsToCalculate)
    return optionsToCalculate;

    
