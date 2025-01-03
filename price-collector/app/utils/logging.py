from functools import wraps
from flask import request

def log_request(action=None):
    def decorator(func):
        @wraps(func)
        def wrapper(self, country: str = None, id: str = None):
            log_action = action or func.__name__
            print(request.remote_addr, f'{log_action}', country, id)
            return func(self, country, id)
        return wrapper
    return decorator
