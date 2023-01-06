from GetOptionsChain.GetOptions import updateAllOptions 
from GetOptionsChain.GetHistoricalReturns import updateAllUnderlyingSecuritiesInfo
import datetime
import pycron

cronJobContainer = {
    'fetch': {
        'startMessage': 'Starting Options Cron',
        'function': updateAllOptions
    },
    'returns': {
        'startMessage': 'Starting Historical Returns Cron',
        'function': updateAllUnderlyingSecuritiesInfo
    },

}

def cronJobInit():
    if pycron.is_now('*/5 * * * *') == True:
        print('Cron job for options fetch starting at: ', datetime.datetime.now(), '');
        cronJobContainer['fetch']['function']();
        print('Cron Job Options Complete for time: ', datetime.datetime.now(), '');

    elif pycron.is_now('*/10 * * * *') == True:
        print(cronJobContainer['returns']['startMessage']);
        cronJobContainer['returns']['function']()
        print('Cron Job Historical Returns Complete for time: ', datetime.datetime.now(), '');

    else: return None;