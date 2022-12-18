from GetOptionsChain.GetOptions import updateAllOptions, updateOptionsData
from GetOptionsChain.Model import getRiskFreeRate, getPriceQuote,getDividendHistory
from multiprocessing import freeze_support

def main():
    quoteSummary = getDividendHistory('AAPL');
    print(quoteSummary);
    # treasuryRate = getRiskFreeRate();
    # print(treasuryRate);
    # updateAllOptions();

if __name__ == '__main__':
    # freeze_support();
    main();