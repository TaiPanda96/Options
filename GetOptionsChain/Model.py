import datetime 
import requests 
import traceback 

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


def getRiskFreeRate():
    """ This function returns the risk free rate. """
    url = 'https://www.cnbc.com/quotes/US10Y'
    headers = { 
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
        'authority': 'www.cnbc.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
        'accept': 'application/json, text/plain, */*',
        'sec-ch-ua-mobile': '?0',
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    except Exception as e:
        print(e)
        traceback.print_exc(exec_info=True)


def getPublicylyListedHolidays():
    return {
        "numberOfTradingDays": 260 - len(holidays),
        "numberOfHolidays": len(holidays),
        "holidays": holidays
    }


def getDividends(symbol):
    """ This function checks for the dividend history of a given stock symbol. """
    try:
        url = "https://query1.finance.yahoo.com/v7/finance/download/{0}?period1=0&period2=9999999999&interval=1d&events=div".format(
            symbol)
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        print(e)
        traceback.print_exc(exec_info=True)


def modelCalculator(symbol, method = 'Black-Scholes', hasDividends = False):
    """ This function calculates the model for the given stock symbol. """
    return
