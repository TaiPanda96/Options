from GetOptionsChain.GetOptions import updateAllOptions 
from GetOptionsChain.GetHistoricalReturns import updateAllUnderlyingSecuritiesInfo
from GetOptionsChain.Model import updateAllModelCalculatedOptions

import pycron
import datetime 
from multiprocessing import freeze_support

cronJobContainer = {
    'Options Cron': {
        'startMessage': 'Starting Options Cron',
        'function': updateAllOptions,
        'freeze_support': True,
    },
    'Options Calculator': {
        'startMessage': 'Starting Options Calculator Cron',
        'function': updateAllModelCalculatedOptions,
        'freeze_support': True,
    },
    'Historical Returns': {
        'startMessage': 'Starting Historical Returns Cron',
        'function': updateAllUnderlyingSecuritiesInfo,
        'freeze_support': False,
    },

}


def historicalReturnsCronJob():
    print(cronJobContainer['Historical Returns']['startMessage']);
    cronJobContainer['Historical Returns']['function']()
    print('Cron Job Historical Returns Complete for time: ', datetime.datetime.now(), '');

def optionsFetchCronJob():
    freeze_support();
    cronJobContainer['Options Calculator']['function']();
    print('Cron Job Options Calculator Complete for time: ', datetime.datetime.now(), '');

def optionsCalculatorCronJob():
    print('Starting Options Calculator Cron');
    freeze_support();
    updateAllModelCalculatedOptions();
    print('Cron Job Options Calculator Complete for time: ', datetime.datetime.now(), '');
