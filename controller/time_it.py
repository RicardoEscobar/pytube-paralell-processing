"""This decorator prints the execution time for the decorated function in minutes:seconds."""
# add the project root directory to the system path
if __name__ == "__main__":
    from pathlib import Path

    project_directory = Path(__file__).parent.parent
    import sys

    # sys.path.insert(0, str(project_directory))
    sys.path.append(str(project_directory))

import time
import functools
from pathlib import Path

from controller.create_logger import create_logger

# Create a logger for this module.
module_logger = create_logger(
    logger_name="controller.time_it",
    logger_filename="time_it.log",
    log_directory=Path(__file__).parent.parent / "logs",
    add_date_to_filename=False,
)


def time_it(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        duration = end - start
        module_logger.info(
            f"{func.__name__} took {(duration) :.2f} seconds. ({seconds_to_minutes(duration)}) minutes"
        )
        return result

    return wrapper


def seconds_to_minutes(seconds):
    """Convert seconds to minutes:seconds."""
    minutes = seconds // 60
    seconds %= 60
    return f"{int(minutes)}:{int(seconds)}"
