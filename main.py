from CronJobContainer.CronJobController import cronJobInit
import time 
# This is the main entry point for the application and will run the cron job every 60 seconds.
# On Windows the subprocesses will import (i.e. execute) the main module at start. You need to insert an if __name__ == '__main__': guard in the main module to avoid creating subprocesses recursively.
if __name__ == '__main__':
    while (1):
        cronJobInit();
        time.sleep(30)