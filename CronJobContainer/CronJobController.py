from GetOptionsChain.GetOptions import updateAllOptions 
from GetOptionsChain.GetHistoricalReturns import updateAllUnderlyingSecuritiesInfo
from GetOptionsChain.Model import updateAllModelCalculatedOptions
import datetime
import pycron
from multiprocessing import freeze_support

cronJobContainer = {
    'fetch': {
        'startMessage': 'Starting Options Cron',
        'function': updateAllOptions,
        'freeze_support': True,
    },
    'calculator': {
        'startMessage': 'Starting Options Calculator Cron',
        'function': updateAllModelCalculatedOptions,
        'freeze_support': True,
    },
    'returns': {
        'startMessage': 'Starting Historical Returns Cron',
        'function': updateAllUnderlyingSecuritiesInfo,
        'freeze_support': False,
    },

}

def cronJobInit():
    if pycron.is_now('*/5 * * * *') == True:
        print('Cron job for options fetch starting at: ', datetime.datetime.now(), '');
        freeze_support();
        cronJobContainer['fetch']['function']();
        print('Cron Job Options Complete for time: ', datetime.datetime.now(), '');

    elif pycron.is_now('*/10 * * * *') == True:
        print(cronJobContainer['calculator']['startMessage']);
        freeze_support();
        cronJobContainer['calculator']['function']();
        print('Cron Job Calculator completed: ', datetime.datetime.now(), '');

    elif pycron.is_now('*/15 * * * *') == True:
        print(cronJobContainer['returns']['startMessage']);
        cronJobContainer['Historical Returns']['function']()
        print('Cron Job Historical Returns Complete for time: ', datetime.datetime.now(), '');

    else: return None;