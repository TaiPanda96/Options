from GetOptionsChain.GetOptions import initOptionsController
from GetOptionsChain.HistoricalReturns import updateAllUnderlyingSecuritiesInfo
import pycron 

cronJobContainer = {
    'Options Cron': {
        'startMessage': 'Starting Options Cron',
        'cronString': '30 * * * *',
        'function': initOptionsController,
    },
    'Historical Returns': {
        'startMessage': 'Starting Historical Returns',
        'cronString': '30 * * * *',
        'function': updateAllUnderlyingSecuritiesInfo,
    }
}

def cronJobInit():
    if pycron.is_now('30 * * * *'):
        print(cronJobContainer['Options Cron']['startMessage']);
        cronJobContainer['Options Cron']['function']()

    if pycron.is_now('30 * * * *'):
        print(cronJobContainer['Historical Returns']['startMessage']);
        cronJobContainer['Historical Returns']['function']()