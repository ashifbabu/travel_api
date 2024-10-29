import time
from functools import wraps
import random
def retry_with_backoff(retries=3, backoff_in_seconds=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            x = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if x == retries:
                        raise e
                    sleep = (backoff_in_seconds * 2 ** x + 
                             random.uniform(0, 1))
                    time.sleep(sleep)
                    x += 1
        return wrapper
    return decorator