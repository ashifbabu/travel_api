import time
from functools import wraps

class RateLimiter:
    def __init__(self, calls, period):
        self.calls = calls
        self.period = period
        self.last_reset = time.time()
        self.num_calls = 0

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_time = time.time()
            if current_time - self.last_reset >= self.period:
                self.num_calls = 0
                self.last_reset = current_time
            
            if self.num_calls >= self.calls:
                raise Exception("Rate limit exceeded")
            
            self.num_calls += 1
            return func(*args, **kwargs)
        return wrapper