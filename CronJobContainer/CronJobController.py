from GetOptionsChain.GetOptions import updateAllOptions
from GetOptionsChain.HistoricalReturns import updateAllUnderlyingSecuritiesInfo

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
    }
}

def cronJobInit():
    if pycron.is_now('*/10 * * * *') == True:
        print(cronJobContainer['Options Cron']['startMessage']);
        freeze_support();
        cronJobContainer['Options Cron']['function']()
        print('Cron Job Options Complete for time: ', datetime.datetime.now(), '');
    else: return None;


def cronJobHistoricalReturns():
    if pycron.is_now('/15 * * * *') == True:
        print(cronJobContainer['Historical Returns']['startMessage']);
        cronJobContainer['Historical Returns']['function']()
        print('Cron Job Historical Returns Complete for time: ', datetime.datetime.now(), '');
    else: return None;


