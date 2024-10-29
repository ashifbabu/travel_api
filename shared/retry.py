import time
from functools import wraps
from typing import Any, Callable


def retry_with_backoff(retries: int = 3, backoff_in_seconds: int = 1) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            x = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if x == retries:
                        raise e
                    sleep = backoff_in_seconds * 2**x
                    time.sleep(sleep)
                    x += 1

        return wrapper

    return decorator
