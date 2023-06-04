"""This is an example of a callback function."""

def add_numbers(x, y, callback):
    """Add two numbers and pass the result to a callback function."""
    result = x + y
    callback(result)

def print_result(result):
    """Print the result of the add_numbers function."""
    print(f"The result is {result}")

add_numbers(5, 10, print_result)
