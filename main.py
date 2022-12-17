from GetOptionsChain.GetOptions import updateAllOptions, updateOptionsData
from multiprocessing import freeze_support

def main():
    updateAllOptions();

if __name__ == '__main__':
    freeze_support();
    main();