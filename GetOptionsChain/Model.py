import datetime 
import requests 
import traceback 


def getRiskFreeRate():
    return 


def getPublicylyListedHolidays():
    return 


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
