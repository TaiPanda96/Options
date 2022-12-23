from   scipy.stats import norm
import datetime 
import numpy as np
import pytz
from datetime import timedelta


def normalDistributionCDF(x, mu = 0, std = 1):
    return norm.cdf(x, mu, std);

def laPlaceCDF(x, mu = 0, std = 1):
    return 0.5 * (1 + np.tanh((x - mu) / (2 * std)));

def calculateRecipeValues(S, X, D, std, T, r, t, t1):
    timeToExpiration     = (T - t).days
    if timeToExpiration == 0 or timeToExpiration < 0: return 0, 0, 0, 0;
    firstTerm            = np.log((S - D * np.exp(r * -1 * timeToExpiration))/X);
    secondTerm           = (r + (std ** 2) / 2) * (timeToExpiration);

    a1 = (firstTerm + secondTerm) / (std * np.sqrt(timeToExpiration));
    a2 = a1 - (std * np.sqrt(timeToExpiration));

    timeToExpiration = (t1 - t).days;
    b1 = np.log((S - D * np.exp(r * -1 * 2 ))/S) + (r + (std ** 2) / 2) * timeToExpiration;
    b2 = b1 - (std * np.sqrt(((T - t).days)));

    return a1, a2, b1, b2;

def calculateEuropeanOptions(calculationObj = {}):
    tradingDays = calculationObj['tradingDays'];
    S     = calculationObj['stockPrice'];
    X     = calculationObj['strike'];
    r     = calculationObj['riskFreeRate'];
    T     = calculationObj['expiration'];
    std   = calculationObj['impliedVolatility'];
    t     = pytz.utc.localize(datetime.datetime.now());

    mU   = calculationObj['logReturns'];
    mStd = calculationObj['standardDeviation'];

    timeToExpiration = (T - t).days / tradingDays;
    if timeToExpiration == 0 or timeToExpiration < 0: return None;
    d1 = (np.log(S/X) + (r + (std ** 2) / 2) * timeToExpiration) / (std * np.sqrt(timeToExpiration));
    d2 = d1 - (std * np.sqrt(timeToExpiration));

    if calculationObj['type'] == 'call':
        callPrice = float(S * laPlaceCDF(d1,mU, mStd) - X * np.exp(-r * timeToExpiration) * laPlaceCDF(d2,mU,mStd));
        return callPrice;

    if calculationObj['type'] == 'put':
        putPrice = float(X * np.exp(-r * timeToExpiration) * laPlaceCDF(-d2,mU, mStd) - S * laPlaceCDF(-d1,mU, mStd));
        return putPrice;
