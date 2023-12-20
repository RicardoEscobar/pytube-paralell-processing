"""This decorator prints the execution time for the decorated function in minutes:seconds."""
# add the project root directory to the system path
if __name__ == "__main__":
    from pathlib import Path

    project_directory = Path(__file__).parent.parent
    import sys

    # sys.path.insert(0, str(project_directory))
    sys.path.append(str(project_directory))

import time
import datetime
from functools import wraps
import logging

from controller.create_logger import create_logger

# Create a logger for this module
module_logger = create_logger(
    logger_name="controller.time_it",
    logger_filename="time_it.log",
    log_directory="logs",
    add_date_to_filename=False,
    console_logging=True,
    console_log_level=logging.INFO,
)


def time_it(func):
    """Decorator to time function calls."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper function for time_it decorator."""
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        duration_seconds = end_time - start_time
        duration_formatted = str(datetime.timedelta(seconds=duration_seconds))
        module_logger.info(
            "Function %s took %s to complete.",
            func.__name__,
            duration_formatted,
        )
        return result

    return wrapper


if __name__ == "__main__":
    @time_it
    def test_function():
        """Test function for time_it decorator."""
        time.sleep(1)


    test_function()
