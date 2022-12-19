from GetOptionsChain.GetOptions import updateAllOptions, updateOptionsData
from GetOptionsChain.Model import getRiskFreeRate, getPriceQuote,getDividendHistory
from GetOptionsChain.HistoricalReturns import getHistoricalYahooPrices, updateAllUnderlyingSecuritiesInfo
from multiprocessing import freeze_support
import datetime

def main():
    updateAllUnderlyingSecuritiesInfo();
    # quoteSummary = getDividendHistory('AAPL');
    # print(quoteSummary);
    # quoteSummary = getHistoricalPrices('AAPL');
    # print(quoteSummary);
    # treasuryRate = getRiskFreeRate();
    # print(treasuryRate);
    # updateAllOptions();
    # logReturns = getHistoricalYahooPrices('AAPL');
    # print(logReturns);

if __name__ == '__main__':
    # freeze_support();
    main();