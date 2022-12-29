from CronJobContainer.CronJobController import cronJobContainer
from multiprocessing import freeze_support
import time 
# This is the main entry point for the application and will run the cron job every 60 seconds.
# On Windows the subprocesses will import (i.e. execute) the main module at start. You need to insert an if __name__ == '__main__': guard in the main module to avoid creating subprocesses recursively.
if __name__ == '__main__':
    while True:
        for cronJob in cronJobContainer:
            if cronJobContainer[cronJob]['freeze_support'] == True:
                freeze_support()
            cronJobContainer[cronJob]['function']()
        time.sleep(120000);