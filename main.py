from GetOptionsChain.GetOptions import updateAllOptions, updateOptionsData
from GetOptionsChain.Model import getRiskFreeRate
from multiprocessing import freeze_support

def main():
    getRiskFreeRate();
    # updateAllOptions();

if __name__ == '__main__':
    # freeze_support();
    main();