from GetOptionsChain.GetOptions import updateAllOptions 
from GetOptionsChain.GetHistoricalReturns import updateAllUnderlyingSecuritiesInfo
from GetOptionsChain.RemoveOldOptions import removeOldOptions
from GetOptionsChain.Model import updateAllModelCalculatedOptions

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
    'Remove Old Data': {
        'startMessage': 'Starting Remove Old Data Cron',
        'function': removeOldOptions,
        'freeze_support': False,
    },
}

