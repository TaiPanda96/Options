import functools
import time 
import pytz 
# https://stackoverflow.com/questions/373335/how-do-i-get-a-cron-like-scheduler-in-python
def repeatEveryDay(func, *args, **kwargs):
    """ 
    This function repeats a given function every day. 
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        # Executable function 
        func(*args, **kwargs)

    return wrapper