"""
Purpose: Task 3 - Count non-space characters.
"""
from utils import simple_decorator

@simple_decorator
def count_non_spaces(text):
    """Counts characters that are not spaces."""
    count = 0
    for c in text:
        if not c.isspace():
            count += 1
    return count