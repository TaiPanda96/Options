import requests
import traceback
import datetime
import time
import numpy as np
import pytz
from bs4 import BeautifulSoup
from Postgres.InsertQuery import insertQuery
from multiprocessing import Pool

headers = { 
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    'authority': 'www.cnbc.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
    'accept': 'application/json, text/plain, */*',
    'sec-ch-ua-mobile': '?0',
}


def getHistoricalPrices(symbol):
    """ This function returns the historical prices for a given stock symbol. """
    url = 'https://api.nasdaq.com/api/quote/{}/chart?assetclass=stocks'.format(symbol)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            quoteStore = response.json() if response else None;
            if quoteStore is None: return None;
            quote = quoteStore.get('data', {});
            historicalPrices = quote['chart'];
            return historicalPrices
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
            if priceContainer is None: 
                print('no price')
                return 
            price = priceContainer.find('span', class_='QuoteStrip-lastPrice');
            if price is not None: return float(price.text.strip().replace('%', '')) / 100;
            else: 
                print('no price')
                return None
        else:
            print('Error Risk Free Rate: ', response.status_code)
            return None

    except Exception as e:
        print(e);


def getHistoricalYahooPrices(symbol=None):
    """ 
    This function returns historical log returns for a given stock symbol. 
    """
    if symbol is None: symbol = 'AAPL';
    today        = int(datetime.datetime.today().timestamp());
    fiveYearsAgo = int(today - (5 * 365 * 24 * 60 * 60));
    url = 'https://query1.finance.yahoo.com/v8/finance/chart/{}?formatted=true&crumb=tVWDTWvaSdP&lang=en-US&region=US&includeAdjustedClose=true&interval=1mo&period1={}&period2={}&events=capitalGain%7Cdiv%7Csplit&useYfid=true&corsDomain=finance.yahoo.com'.format(symbol, fiveYearsAgo, today);
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            quoteStore = response.json() if response else None;
            if quoteStore is None: return None;
            quote = quoteStore.get('chart', {}).get('result', [])[0];
            if quote is None: return None;
            historicalPrices = quote.get('indicators', {}).get('quote',{});
            closePrices      = historicalPrices[0].get('close',{}) if historicalPrices[0] else None;

            if closePrices is None: return None

            # Calculate log returns
            logReturns        = list((np.log(closePrices[i] / closePrices[i-1])) for i in range(1, len(closePrices)));
            avgReturns        = sum(logReturns) / len(logReturns);
            standardDeviation = np.std(logReturns);

            return { 
                'symbol': symbol,
                'avgLogReturns': float(avgReturns) if avgReturns is not None else None,
                'standardDeviation': float(standardDeviation) if standardDeviation is not None else None,
                'timestamp': pytz.utc.localize(datetime.datetime.fromtimestamp(today).now())
            }
        else:
            return None
    except Exception as e:
        print(e)
        traceback.print_exc()


def updateRiskFreeRate():
    """ This function updates the risk free rate. """
    # Get risk rating 
    try: 
        riskFreeRate = getRiskFreeRate();
        if riskFreeRate: 
            riskFreeRateObj = {
                'timestamp': pytz.utc.localize(datetime.datetime.now()),
                'riskFreeRate': riskFreeRate
            }
            useColumns = list(riskFreeRateObj.keys());
            update     = [tuple(riskFreeRateObj.values())];
            # Insert the results into the database
            insertQuery('risk_free_rate', useColumns, update);
            print('Updated risk free rate returns for', datetime.datetime.now());
    
    except Exception as error: 
        print(error)
        traceback.print_exc();


def updateAllUnderlyingSecuritiesInfo():
    """ This function updates the underlying securities info. """
    # Get all the underlying securities
    tickers    = ['AAPL', 'TSLA', 'AMZN', 'GOOGL', 'TSMC', 'META'];
    useColumns = ['symbol', 'avgLogReturns', 'standardDeviation', 'timestamp'];
    results    = [];
    for ticker in tickers:
        logReturns = getHistoricalYahooPrices(ticker);
        if logReturns is not None:
            results.append(logReturns);
        time.sleep(1);

    update = [tuple(result.values()) for result in results]
    # Insert the results into the database
    insertQuery('historical_returns', useColumns, update);
    print('Updated historical returns for all underlying securities.');