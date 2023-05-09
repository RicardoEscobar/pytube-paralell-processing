"""This decorator prints the execution time for the decorated function in minutes:seconds."""
import time
import functools


def time_it(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        duration = end - start
        print(f'{func.__name__} took {(duration) :.2f} seconds. ({seconds_to_minutes(duration)}) minutes')
        return result
    return wrapper

def seconds_to_minutes(seconds):
    """Convert seconds to minutes:seconds."""
    minutes = seconds // 60
    seconds %= 60
    return f'{int(minutes)}:{int(seconds)}'