from GetOptionsChain.Model import updateAllModelCalculatedOptions
from multiprocessing import freeze_support

if __name__ == '__main__':
    freeze_support();
    updateAllModelCalculatedOptions();