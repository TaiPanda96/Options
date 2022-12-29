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
    'Historical Returns': {
        'startMessage': 'Starting Historical Returns Cron',
        'function': updateAllUnderlyingSecuritiesInfo,
        'freeze_support': False,
    },
    'Options Calculator': {
        'startMessage': 'Starting Options Calculator Cron',
        'function': updateAllModelCalculatedOptions,
        'freeze_support': True,
    },
}

def cronJobInit():
    if pycron.is_now('*/10 * * * *') == True:
        print(cronJobContainer['Options Cron']['startMessage']);
        freeze_support();
        cronJobContainer['Options Cron']['function']();
        cronJobContainer['Options Calculator']['function']();
        print('Cron Job Options Complete for time: ', datetime.datetime.now(), '');

    elif pycron.is_now('*/15 * * * *') == True:
        print(cronJobContainer['Historical Returns']['startMessage']);
        cronJobContainer['Historical Returns']['function']()
        print('Cron Job Historical Returns Complete for time: ', datetime.datetime.now(), '');

    else: return None;

