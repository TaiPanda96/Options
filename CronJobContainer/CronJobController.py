from GetOptionsChain.GetOptions import updateAllOptions 
from GetOptionsChain.GetHistoricalReturns import updateAllUnderlyingSecuritiesInfo
from GetOptionsChain.RemoveOldOptions import removeOldOptions
from GetOptionsChain.Model import modelCalculator

from   multiprocessing import freeze_support
import pycron 
import datetime 

cronJobContainer = {
    'Options Cron': {
        'startMessage': 'Starting Options Cron',
        'function': updateAllOptions,
        'freeze_support': True,
    },
    'Historical Returns': {
        'startMessage': 'Starting Historical Returns Cron',
        'function': updateAllUnderlyingSecuritiesInfo,
    },
    'Remove Old Data': {
        'startMessage': 'Starting Remove Old Data Cron',
        'function': removeOldOptions 
    },
    'Options Calculator': {
        'startMessage': 'Starting Options Calculator Cron',
        'function': modelCalculator
    }
}

def cronJobInit():
    if pycron.is_now('*/10 * * * *') == True:
        print(cronJobContainer['Options Cron']['startMessage']);
        freeze_support();
        cronJobContainer['Options Cron']['function']()
        print('Cron Job Options Complete for time: ', datetime.datetime.now(), '');

    if pycron.is_now('*/11 * * * *') == True:
        print(cronJobContainer['Remove Old Data']['startMessage']);
        cronJobContainer['Remove Old Data']['function']()
        print('Cron Job Remove Old Data Complete for time: ', datetime.datetime.now(), '');

    elif pycron.is_now('*/15 * * * *') == True:
        print(cronJobContainer['Historical Returns']['startMessage']);
        cronJobContainer['Historical Returns']['function']()
        print('Cron Job Historical Returns Complete for time: ', datetime.datetime.now(), '');

    elif pycron.is_now('*/20 * * * *') == True:
        print(cronJobContainer['Options Calculator']['startMessage']);
        cronJobContainer['Options Calculator']['function']()
        print('Cron Job Options Calculator Complete for time: ', datetime.datetime.now(), '');

    else: return None;

