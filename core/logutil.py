import logging
from functools import wraps

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] : %(message)s')

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)

    logger.addHandler(ch)
    return logger

def format_api_error(response_data):
    exc_str = ''
    for key, value in response_data['error'].items():
        exc_str += f'{key} : {value}, '
    if exc_str.endswith(', '):
        exc_str = exc_str[:-2]
    return exc_str

def log_exception(logger: logging.Logger, exception_case=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                logger.exception(f'Exception in function {func}')
                if exception_case:
                    if callable(exception_case):
                        return exception_case(*args, **kwargs)
                    return exception_case
                raise
        return wrapper
    return decorator
