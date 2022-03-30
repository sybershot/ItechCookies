import errno
import os
import time

from functools import wraps


def waituntiltrue(func, timeout=2, error_message=os.strerror(errno.ETIME)):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        while time.time() < start + timeout:
            if bool(func(*args, **kwargs)):
                return True
            else:
                continue
        return False
    return wrapper
