from scipy.stats import norm
import datetime 
import numpy as np
import pytz


def laplaceDistributionCDF(x, mu, b):
    return (1/2 * (1 + np.sign(x - mu) * (1 - np.exp(-1 * abs(x - mu) / b))))


def normalDistributionCDF(x):
    return norm.cdf(x)


def calculatea1a2b1b2(stockPrice, strikePrice, dividendsInequality, std, expirationDate, riskFreeRate, tradingDays = 248):
    timediff = expirationDate - pytz.utc.localize(datetime.datetime.now());
    T  = timediff.days / tradingDays;
    r  = riskFreeRate
    a1 = (np.log(stockPrice - dividendsInequality/ strikePrice) + (r + std ** 2 / 2) * T) / (std * np.sqrt(T))
    a2 = a1 - std * np.sqrt(T)
    b1 = (np.log(stockPrice - dividendsInequality / strikePrice) + (r - std ** 2 / 2) * T) / (std * np.sqrt(T))
    b2 = b1 - std * np.sqrt(T)
    return a1, a2, b1, b2

